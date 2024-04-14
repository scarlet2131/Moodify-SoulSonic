# This is a sample Python script.

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import auth_spotify
# Adjust imports based on your directory structure
from app.api.v1.music.auth import router as auth_router
from app.api.v1.music.emotion import router as emotion_router
from app.core.questions import QUESTIONS, USER_INFO_QUESTIONS

app = FastAPI()

# Serving Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 Templates
templates = Jinja2Templates(directory="templates")
@app.get("/register")
async def show_register(request: Request):  # Corrected type annotation
    # Use the templates object to render the HTML page
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login")
async def show_login(request: Request):  # Corrected type annotation
    # Use the templates object to render the HTML page
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/")
async def show_login(request: Request):  # Corrected type annotation
    # Use the templates object to render the HTML page
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/history")
async def show_login(request: Request):  # Corrected type annotation
    # Use the templates object to render the HTML page
    return templates.TemplateResponse("history.html", {"request": request})

@app.get("/resetPassword")
async def show_login(request: Request):  # Corrected type annotation
    # Use the templates object to render the HTML page
    return templates.TemplateResponse("resetPassword.html", {"request": request})

@app.get("/home")
async def get_index_page(request: Request):
    # Pass the questions to the template
    return templates.TemplateResponse("home.html", {
        "request": request,
        "questions": QUESTIONS,
        "user_info_questions": USER_INFO_QUESTIONS
    })


# Including Routers
app.include_router(auth_router, prefix="/api/v1/music")
app.include_router(emotion_router, prefix="/api/v1/music")
app.include_router(auth_spotify.router)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
