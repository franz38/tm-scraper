from bs4 import BeautifulSoup

def get_box(soup: BeautifulSoup, query: str) -> BeautifulSoup:
    boxes = soup.find_all(class_="box")
    for box in boxes:
        h = box.find(class_="content-box-headline")
        if h and query in h.get_text().strip().lower():
            return box