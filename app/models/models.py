from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float, ARRAY, Enum, TIMESTAMP, JSON
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

    # New column for role
    role = Column(Enum("admin", "user", name="user_roles"), nullable=False, server_default="user")

    # Relationship with carts
    carts = relationship("Cart", back_populates="user")


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    total_amount = Column(Float, nullable=False)

    # Relationship with user
    user = relationship("User", back_populates="carts")

    # Relationship with cart items
    cart_items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relationship with cart and product
    cart = relationship("Cart", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")




class GrandCategory(Base):
    __tablename__ = "grand_categories"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship with parent categories
    parent_categories = relationship("ParentCategory", back_populates="grand_category", cascade="all, delete-orphan")


class ParentCategory(Base):
    __tablename__ = "parent_categories"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    image_path = Column(String, nullable=True)  # Optional image path for Parent Category

    # Foreign key to GrandCategory
    grand_category_id = Column(Integer, ForeignKey("grand_categories.id", ondelete="CASCADE"), nullable=False)

    # Relationship with grand category
    grand_category = relationship("GrandCategory", back_populates="parent_categories")

    # Relationship with child categories
    child_categories = relationship("ChildCategory", back_populates="parent_category", cascade="all, delete-orphan")


class ChildCategory(Base):
    __tablename__ = "child_categories"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    # Foreign key to ParentCategory
    parent_category_id = Column(Integer, ForeignKey("parent_categories.id", ondelete="CASCADE"), nullable=False)

    # Relationship with parent category
    parent_category = relationship("ParentCategory", back_populates="child_categories")

    # Relationship with products
    products = relationship("Product", back_populates="child_category", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    discount_percentage = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    brand = Column(String, nullable=False)
    thumbnail = Column(String, nullable=False)
    images = Column(ARRAY(String), nullable=False)
    is_published = Column(Boolean, server_default="True", nullable=False)
    # created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)
    favourite = Column(Boolean, nullable=False)
    recomended = Column(Boolean, nullable=False)

    # Foreign key to ChildCategory
    child_category_id = Column(Integer, ForeignKey("child_categories.id", ondelete="CASCADE"), nullable=False)

    # Relationship with child category
    child_category = relationship("ChildCategory", back_populates="products")

    # Relationship with cart items
    cart_items = relationship("CartItem", back_populates="product")


    # Relationship with cart items
    cart_items = relationship("CartItem", back_populates="product")


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    title = Column(String, nullable=False)
    text = Column(String, nullable=False)
    image = Column(String, nullable=False)



# class HeaderTabs(Base):
#     __tablename__ = "header_tab"

#     id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
#     name = Column(String, unique=True, nullable=False)
    
#     # Relationship with SubHeaderTabs
#     sub_header_tabs = relationship("SubHeaderTabs", back_populates="header_tab", cascade="all, delete")


# class SubHeaderTabs(Base):
#     __tablename__ = "sub_header_tabs"

#     id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
#     name = Column(String, unique=True, nullable=False)

#     # Relationship with HeaderTabs
#     header_tab_id = Column(Integer, ForeignKey('header_tab.id', ondelete="CASCADE"), nullable=False)
#     header_tab = relationship("HeaderTabs", back_populates="sub_header_tabs")

#     # Relationship with HeaderProducts
#     header_products = relationship("HeaderProducts", back_populates="sub_header_tabs", cascade="all, delete")
#     header_articles = relationship("HeaderArticles", back_populates="sub_header_tabs")



# class HeaderProducts(Base):
#     __tablename__ = "header_products"

#     id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
#     title = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     price = Column(Integer, nullable=False)
#     discount_percentage = Column(Float, nullable=False)
#     rating = Column(Float, nullable=False)
#     stock = Column(Integer, nullable=False)
#     brand = Column(String, nullable=False)
#     thumbnail = Column(String, nullable=False)
#     images = Column(ARRAY(String), nullable=False)
#     is_published = Column(Boolean, server_default="True", nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

#     # Relationship with SubHeaderTabs
#     sub_header_tabs_id = Column(Integer, ForeignKey("sub_header_tabs.id", ondelete="CASCADE"), nullable=False)
#     sub_header_tabs = relationship("SubHeaderTabs", back_populates="header_products")


# class HeaderArticles(Base):
#     __tablename__ = "header_articles"

#     id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
#     title = Column(String, nullable=False)
#     content = Column(JSON, nullable=False)  # Use JSON to store structured content
#     created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"), nullable=False)

#     # Allow NULL values for sub_header_tabs_id
#     sub_header_tabs_id = Column(Integer, ForeignKey("sub_header_tabs.id", ondelete="CASCADE"), nullable=True)
#     sub_header_tabs = relationship("SubHeaderTabs", back_populates="header_articles")
