import unicodedata
from rest_framework import serializers
from .models import Item, Product, Feed, RelatedProduct


class UnicodeCharField(serializers.CharField):
    """
        This is the custom serializer field to handle the non-ASCII character to store in postgres database.

        This class is inherited from the Serializer Char Field class

        methods:
            - to_internal_value
    """

    def to_internal_value(self, data):
        """
        This method override the to_internal_value method of serializer.CharField class.
        :param data :(str):
        :return: normalized_data : (str)
        """
        # replace non-ASCII characters with their closest ASCII equivalent
        normalized_data = unicodedata.normalize('NFKD', data if data else "").encode('ascii', 'ignore').decode()
        return super().to_internal_value(normalized_data)


class RelatedProductSerializer(serializers.ModelSerializer):
    """
            This is the Model serializer class for Related Products data.

            instance:
                - model (as this is a model serializer so only provide model)

            methods:
                - to_internal_value
     """

    class Meta:
        model = RelatedProduct
        fields = ('gtin', 'trade_item_unit_descriptor')

    def to_internal_value(self, data):
        """
                This method override the to_internal_value method of ModelSerializer class.
                :param data :(Object):
                :return: normalized_data : (Object)
        """
        data['gtin'] = str(int(data['gtin']))
        return super().to_internal_value(data)


class ItemSerializer(serializers.ModelSerializer):
    """
            This is the Model serializer class for Items.

            instance:
                - model (as this is a model serializer so only provide model)
                - notes (to parsed the notes field data created)
                - type (to parsed the the type field data created)

            methods:
                - to_internal_value
    """
    related_products = RelatedProductSerializer(many=True, allow_null=True, required=False)
    notes = UnicodeCharField(allow_null=True, allow_blank=True, required=False)
    type = UnicodeCharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Item
        fields = '__all__'
        required_fields = ('code',)

    def to_internal_value(self, data):
        """
                This method override the to_internal_value method of ModelSerializer class.
                This method works for request object.
                :param data :(Object):
                :return: normalized_data : (str)
                    there's correction for some data as well. As we declare the field as char and we might receive a boolean so to handle such data use this method.
        """
        # to remove the zero from start in the code before storing to database.
        if data.get('code'):
            data['code'] = str(int(data.get('code')))

        # if there's no type field, it must set None in DB.
        if 'type' not in data:
            data['type'] = None

        # if we 'receive trade_item_descriptor' then transform to 'trade_item_unit_descriptor'
        if 'trade_item_descriptor' in data:
            data['trade_item_unit_descriptor'] = data['trade_item_descriptor']

        # for some records we have category field but missing categ_id
        if 'category' in data:
            data['categ_id'] = data['category_id']
            data['category_id'] = data['category']

        # on database side this is a char field but we receive boolean in data, so I transform to string.
        if 'edeka_article_number' in data and not data.get('edeka_article_number'):
            data['edeka_article_number'] = ""

        return super().to_internal_value(data)

    def to_representation(self, instance):
        """
                This method override the to_representation method of ModelSerializer class.
                This method works for response object.
                :param data :(str):
                :return: normalized_data : (str)
                    there's correction for some data as well. As we declare the field as char and we might receive a boolean so to handle such data use this method.
        """
        data = super().to_representation(instance)

        # on database side this is a char field but we receive boolean for response, so I transform to string.
        if not data['notes']:
            data['notes'] = False
        # on database side this is a char field but we receive boolean for response, so I transform to string.
        if not data['edeka_article_number']:
            data['edeka_article_number'] = False
        return data


class ProductSerializer(serializers.ModelSerializer):
    """
            This is the Model serializer class for Product.

            instance:
                - model (as this is a model serializer so only provide model)
                - item (the Item must be created before product so we can bind it with Product.)

            methods:
                - validate_item
                - create
    """
    item = ItemSerializer(required=True)

    class Meta:
        model = Product
        fields = '__all__'
        required_fields = ['item']
        extra_kwargs = {
            'product_feed': {'required': False},
        }

    def validate_item(self, value):
        """
        Validate the related item instance. It must be validated and presented to create a new product.
        """
        item_serializer = ItemSerializer(data=value)
        if not item_serializer.is_valid():
            raise serializers.ValidationError(item_serializer.errors)
        return value

    def create(self, validated_data):
        """
                This method override the create method of ModelSerializer class.
                This method works for create request object.
                As we have to create or insert data to multiple tables, so we must have to over-ride this method to insert the data.
                :param validated_data :(Object):
                :return: Product : (Object)
        """
        # extract the item object from Product Object
        item_data = validated_data.pop('item')
        # extract the related Products from the Product Object
        related_products_data = item_data.pop('related_products', [])
        try:
            # try to get the existing item with combination of code and type field, if exist then update
            # only provided fields data
            item = Item.objects.get(code=item_data.get("code"), type=item_data.get("type"))
            for attr, value in item_data.items():
                if value:
                    setattr(item, attr, value)
            item.save()
        except Item.DoesNotExist:
            # if item does not exist then create a new one with provided data.
            item = Item.objects.create(**item_data)
        # create a new Product Object and attached an Item object
        prod = Product.objects.create(item=item, **validated_data)

        # for related product we must have Item created before then we can related products to that item as
        # many to many field record.
        for related_product_data in related_products_data:
            if not item.related_products.filter(gtin=related_product_data.get("gtin")).exists():
                related_product = RelatedProduct.objects.create(**related_product_data)
                item.related_products.add(related_product)
        return prod


class DataSerializer(serializers.ModelSerializer):
    """
                This is the Model serializer class for Feed which insert the data from json file.

                instance:
                    - model (as this is a model serializer so only provide model)
                    - Product (the Products must be created before product, so we can bind it with Feed.)

                methods:
                    - create
        """
    amounts = ProductSerializer(many=True)

    class Meta:
        model = Feed
        fields = '__all__'
        required_fields = ['amounts']

    def create(self, validated_data):
        """
                This method override the create method of ModelSerializer class for Feed.
                This method works for create request object.
                As we have to create or insert data to multiple tables, so we must have to over-ride this method to insert the data.
                :param validated_data :(Object):
                :return: Product : (Object)
        """
        # extract the Products list from Feed.
        amounts_data = validated_data.pop('amounts')
        # create the Feed Object from the provided data
        feed = Feed.objects.create(**validated_data)
        for amount_data in amounts_data:
            # extract the item object from Product Object
            item_data = amount_data.pop('item')
            # extract the related Products from the Product Object
            related_products_data = item_data.pop('related_products', [])
            try:
                # try to get the existing item with combination of code and type field, if exist then update
                # only provided fields data
                item = Item.objects.get(code=item_data.get("code"), type=item_data.get("type"))
                for attr, value in item_data.items():
                    setattr(item, attr, value)
                item.save()
            except Item.DoesNotExist:
                # if item does not exist then create a new one with provided data.
                item = Item.objects.create(**item_data)

            # create a new Product Object and attached an Item object
            Product.objects.create(product_feed=feed, item=item, **amount_data)

            # for related product we must have Item created before then we can related products to that item as
            # many to many field record.
            for related_product_data in related_products_data:
                if not item.related_products.filter(gtin=related_product_data.get("gtin")).exists():
                    related_product = RelatedProduct.objects.create(**related_product_data)
                    item.related_products.add(related_product)
        return feed
