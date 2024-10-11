from datetime import datetime

from apps.app import db


class FirstCategory(db.Model):
    __tablename__ = 'first_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # SecondCategoryとのリレーションを定義する
    SecondCategory = db.relationship('SecondCategory', back_populates='FirstCategory', lazy=True)
    # Itemとのリレーションを定義する
    Item = db.relationship('Item', back_populates='FirstCategory', lazy=True)

    def __str__(self):
        return self.name


class SecondCategory(db.Model):
    __tablename__ = 'second_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    firstcategory_id = db.Column(db.Integer, db.ForeignKey('first_category.id'))
    # FirstCategoryとのリレーションを定義する
    FirstCategory = db.relationship('FirstCategory', back_populates='SecondCategory', lazy=True)
    # ThirdCategoryとのリレーションを定義する
    ThirdCategory = db.relationship('ThirdCategory', back_populates='SecondCategory', lazy=True)
    # Itemとのリレーションを定義する
    Item = db.relationship('Item', back_populates='SecondCategory', lazy=True)

    def __str__(self):
        return self.name


class ThirdCategory(db.Model):
    __tablename__ = 'third_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    secondcategory_id = db.Column(db.Integer, db.ForeignKey('second_category.id'))
    # SecondCategoryとのリレーションを定義する
    SecondCategory = db.relationship('SecondCategory', back_populates='ThirdCategory', lazy=True)
    # Itemとのリレーションを定義する
    Item = db.relationship('Item', back_populates='ThirdCategory', lazy=True)

    def __str__(self):
        return self.name


class ItemCondition(db.Model):
    __tablename__ = 'item_condition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # Itemとのリレーションを定義する
    Item = db.relationship('Item', back_populates='ItemCondition', lazy=True)

    def __str__(self):
        return self.name


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    firstcategory_id = db.Column(db.Integer, db.ForeignKey('first_category.id'))
    secondcategory_id = db.Column(db.Integer, db.ForeignKey('second_category.id'))
    thirdcategory_id = db.Column(db.Integer, db.ForeignKey('third_category.id'), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)
    condition_id = db.Column(db.Integer, db.ForeignKey('item_condition.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    postage = db.Column(db.Integer, nullable=False)
    movie_path = db.Column(db.String(255), nullable=True)
    movieflag = db.Column(db.Boolean, nullable=False, default=False)
    transactionflag = db.Column(db.Boolean, nullable=False, default=False)
    shippingflag = db.Column(db.Boolean, nullable=False, default=False)
    receiptflag = db.Column(db.Boolean, nullable=False, default=False)
    # FirstCategoryとのリレーションを定義する
    FirstCategory = db.relationship('FirstCategory', back_populates='Item', lazy=True)
    # SecondCategoryとのリレーションを定義する
    SecondCategory = db.relationship('SecondCategory', back_populates='Item', lazy=True)
    # ThirdCategoryとのリレーションを定義する
    ThirdCategory = db.relationship('ThirdCategory', back_populates='Item', lazy=True)
    # ItemConditionとのリレーションを定義する
    ItemCondition = db.relationship('ItemCondition', back_populates='Item', lazy=True)
    # Purchaseとのリレーションを定義する
    Purchase = db.relationship('Purchase', back_populates='Item', lazy=True)
    # Imageとのリレーションを定義する
    images = db.relationship('Image', secondary='item_image', back_populates='items')


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255))
    items = db.relationship('Item', secondary='item_image', back_populates='images')


class ItemImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))


class PaymentMethod(db.Model):
    __tablename__ = 'payment_method'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # Purchaseとのリレーションを定義する
    Purchase = db.relationship('Purchase', back_populates='PaymentMethod', lazy=True)

    def __str__(self):
        return self.name


class Purchase(db.Model):
    __tablename__ = 'purchase'
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    paymentmethod_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'))
    shippingaddress = db.Column(db.String(100), nullable=False)
    totalamount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # Itemとのリレーションを定義する
    Item = db.relationship('Item', back_populates='Purchase', lazy=True)
    # PaymentMethodとのリレーションを定義する
    PaymentMethod = db.relationship('PaymentMethod', back_populates='Purchase', lazy=True)
    # CreditCardPayとのリレーションを定義する
    CreditCardPay = db.relationship('CreditCardPay', back_populates='Purchase', lazy=True)
    # AccountTransferPayとのリレーションを定義する
    AccountTransferPay = db.relationship('AccountTransferPay', back_populates='Purchase', lazy=True)


class CreditCardPay(db.Model):
    __tablename__ = 'credit_card_pay'
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    cardnumber = db.Column(db.String(16), nullable=False)
    goodthru = db.Column(db.String(4), nullable=False)
    pin = db.Column(db.String(3), nullable=False)
    cardnominee = db.Column(db.String(20), nullable=False)
    # Purchaseとのリレーションを定義する
    Purchase = db.relationship('Purchase', back_populates='CreditCardPay', lazy=True)


class AccountTransferPay(db.Model):
    __tablename__ = 'account_transfer_pay'
    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    bankcode = db.Column(db.String(4), nullable=False)
    branchcode = db.Column(db.String(3), nullable=False)
    deposititem = db.Column(db.String(1), nullable=False)
    accountnumber = db.Column(db.String(7), nullable=False)
    accountnominee = db.Column(db.String(20), nullable=False)
    # Purchaseとのリレーションを定義する
    Purchase = db.relationship('Purchase', back_populates='AccountTransferPay', lazy=True)