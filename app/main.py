from fastapi.staticfiles import StaticFiles
from app.routers import products, category_grand, category_child, category_parent, carts, users, auth, accounts, blogs, brand
from fastapi import FastAPI


description = """
Welcome to the E-commerce API! 🚀

This API provides a comprehensive set of functionalities for managing your e-commerce platform.

Key features include:

- **Crud**
	- Create, Read, Update, and Delete endpoints.
- **Search**
	- Find specific information with parameters and pagination.
- **Auth**
	- Verify user/system identity.
	- Secure with Access and Refresh tokens.
- **Permission**
	- Assign roles with specific permissions.
	- Different access levels for User/Admin.
- **Validation**
	- Ensure accurate and secure input data.


For any inquiries, please contact:

"""


app = FastAPI(
    description=description,
    title="E-commerce API",
    version="1.0.0",
    contact={
        "name": "Ecommerce API",
    },
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai",
        "layout": "BaseLayout",
        "filter": True,
        "tryItOutEnabled": True,
        "onComplete": "Ok"
    },
)


app.include_router(products.router)
app.include_router(category_grand.router)
app.include_router(category_parent.router)
app.include_router(category_child.router)
app.include_router(brand.router)
app.include_router(carts.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(auth.router)
app.include_router(blogs.router)

