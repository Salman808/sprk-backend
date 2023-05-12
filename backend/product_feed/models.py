from django.db import models


class Feed(models.Model):
    """
    This is Feed django ORM model class. The use of this model is minimalistic and only utilised to upload the products
    data as feed.

    :param
        - supplier_id : str (to store the supplier id in database)
        - user_id : str (to store the user id in database)
        - session_id : str (to store the session id in database)
        - session_start_time : str (to store the session start time stamp from the provided Feed)
        - session_end_tine : DateTime (to store the session end time stamp from the provided Feed)
    """
    supplier_id = models.CharField()
    user_id = models.CharField()
    session_id = models.CharField()
    session_start_time = models.DateTimeField()
    session_end_time = models.DateTimeField()


class RelatedProduct(models.Model):
    """
     This is Related Products django ORM model class. This model is used to handle many to many relation among the
     products as related product.

     :param
         - gtin : str (to store related product's item's code as gtin)
         - trade_item_unit_descriptor : str (to store related product's item's trade_item_unit_descriptor)
     """
    gtin = models.CharField(max_length=20)
    trade_item_unit_descriptor = models.CharField(max_length=50)


class Product(models.Model):
    """
        This is Product django ORM model class. This is the main class use for Products insertion. It does have a
        relation with other models.

        :relations
            - Item : ManyToOne (the product class does have Many-to-one relation with Item)
            - Feed : ManyToOne (the product class have a relation with Feed to have the information about the feed)
        :param
            - product_feed_id : Foreign (to store the specified feed information with the product.)
            - amount : int (number or quantity of the product)
            - bbd : DateTime (to store the Best Before date which will use for great purpose for some products)
            - comment : str (to store the comments on the product)
            - country_of_disassembly : str (to store the country information where product dissembled)
            - country_of_slaughter : str (to store the country information where product slaughtered)
            - lot_number : str (to store the Product's lot number if imported)
            - cutting_plant_registration : str (to store the product's cutting plant registration code)
            - item : Object (this is the item Object which tells more about the product)
    """
    product_feed = models.ForeignKey(to=Feed, on_delete=models.CASCADE, related_name='amounts', null=True)
    amount = models.IntegerField()
    bbd = models.DateTimeField(verbose_name="bbd", null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    country_of_disassembly = models.CharField(null=True, blank=True)
    country_of_rearing = models.CharField(null=True, blank=True)
    country_of_slaughter = models.CharField(null=True, blank=True)
    slaughterhouse_registration = models.CharField(null=True, blank=True)
    lot_number = models.CharField(null=True, blank=True)
    cutting_plant_registration = models.CharField(null=True, blank=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)


class Item(models.Model):
    """
        This is Item django ORM model class. This is the main class use for Item insertion. It does have a
        relation with other models. The code and type fields of Item class creates a relation for unique item.

           :relations
               - Product : OneToMany (the Item class does have One-to-Many relation with Product)
               - related_products : ManyToMany (the product class have a many-to-many relation with itself to have the information about the related products)
           :param
               - amount_multiplier : int (to store the product count multiplier)
               - brand : str (it does item's brand information)
               - categ_id : int (this is an integer field to store categ id )
                    I must have to create a seperate category table but I didn't get much information through sample json data.
               - category_id : str (to store the item's category id)
               - code : str (it is the main item's identifier and it is compulsory to provide.)
               - type : str (it is the one of the combine identifier for Item's object.)
               - description : str (to store the Item's description)
               - net_weight : Object (this is a JSON field to store the net_weight because it could be either a number or an object.)
               - gross_weight : Object (this is a JSON field to store the gross_weight because it could be either a number or an object.)
               - hierarchies : Object (this is a JSON field to store the hierarchies)
               - notes : str (to store the notes on the item)
               - edeka_article_number : str (don't have much information about this field.)
               - packaging : str (to store the packaging information of the item.)
               - regulated_name : str (the regualted name of the item)
               - requires_best_before_date : boolean (to store the flag either we need best before date for item or not)
               - requires_meat_info : boolean (to store the flag either we need meat info for item or not)
               - status : str (to store the item's status)
               - trade_item_unit_descriptor: str (to store item unit descriptor, it can be an enum but I prefer to use char field for current scenario)
               - trade_item_unit_descriptor_name: str ( to store item unit descriptor name. we could use a separate table fro unit descriptors but I prefer to use same)
               - unit_name : str (to store the unit name)
               - vat_rate : str(to store the Vate rate information)
               - vat : Object (this is a JSON based field because we can expect an object. But I didn't have a new table because the information could be vary as per item)

    """
    amount_multiplier = models.IntegerField(null=True, blank=True)
    brand = models.CharField(max_length=30, null=True, blank=True)
    categ_id = models.IntegerField(null=True, blank=True)
    category_id = models.CharField(max_length=15, null=True, blank=True)
    code = models.CharField(max_length=20)
    type = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    gross_weight = models.JSONField(null=True, blank=True)
    net_weight = models.JSONField(null=True, blank=True)
    hierarchies = models.JSONField(null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    edeka_article_number = models.CharField(max_length=20, null=True, blank=True)
    packaging = models.CharField(max_length=50, null=True, blank=True)
    regulated_name = models.CharField(max_length=30, null=True, blank=True)
    requires_best_before_date = models.BooleanField(null=True, blank=True, default=False)
    requires_meat_info = models.BooleanField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    trade_item_unit_descriptor = models.CharField(max_length=255, null=True, blank=True)
    trade_item_unit_descriptor_name = models.CharField(max_length=255, null=True, blank=True)
    unit_name = models.CharField(max_length=10, null=True, blank=True)
    validation_status = models.CharField(max_length=20, null=True, blank=True)
    vat_rate = models.CharField(max_length=20, null=True, blank=True)
    related_products = models.ManyToManyField(RelatedProduct, related_name='items')
    vat = models.JSONField(null=True, blank=True)
