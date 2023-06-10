# Standard library imports
from dataclasses import dataclass
from typing import Tuple, List


# Third party imports
import bs4 
import click
import requests
import tabulate 
from fuzzywuzzy import fuzz

# Local application imports
from translate import Translator

# Scraped websites 
KSP = 'https://ksp.co.il/web/cat/'
IVORY = 'https://www.ivory.co.il/catalog.php'
TMS = 'https://tms.co.il/'

@dataclass 
class Item: 
    name: str
    price : int 
    similarty : int | None = None
    url : str | None = None
    description : str | None = None

@click.group()
def cli():
    pass


@cli.command(name='ivory')
@click.argument('name')
@click.option('--description', default='', help='Optional description of the product', type=str)
@click.option('--price', default=0, help='Expected price.', type=int)
@click.option('--count', default=3, help='Number of items returned.') 
def ivory(name : str, description : str, price : int, count : int) -> list[Tuple[Item,int]] | None:
    """ Scrape the item's price from ivory 

    Args:
        item (str): The item to be scraped 

    Returns:
        Item: a list of pair object representing the wanted item and the similarty to the inputted item.
    """

    
    try:
        params = {'act' : 'cat', 'q' : name}
        res = requests.get(IVORY,params=params, timeout=10)
        
        
        if res.status_code == 200: 
            soup = bs4.BeautifulSoup(res.content, 'html.parser')

            # Extracting the prices
            price_elements = soup.findAll('span', class_='price')

            # Extracting the names
            name_elements = soup.findAll('div', class_='title_product_catalog')

            # Extracting all of the URLS
            urls_element = soup.find_all('a', attrs={'data-t-val': ''}, style='color:black;height:100%')

            urls = []
            for element in urls_element:
                urls.append(element['href'])
            
           
            
            item_list : List[Item] = []
            TRANSLATOR = Translator(source='detect language', target='en')
            
            for index in range(len(name_elements)):
                item_name = TRANSLATOR.translate(name_elements[index].text.strip())
                price = price_elements[index].text.strip()
                if ',' in price_elements[index].text.strip():
                    price = ''.join(price.split(','))
                item_price = float(price)
                item_list.append(Item(name=item_name, price=item_price, url=urls[index]))
            
            for item in item_list:
                item_page = requests.get(item.url)
                soup = bs4.BeautifulSoup(item_page.content, 'html.parser')
                description_element = soup.find('div', id="productMainBlock")
                description_element = description_element.find('h2')
                item_description = TRANSLATOR.translate(description_element.text.strip())
                item.description = item_description
                
    
            TRANSLATOR.quit()

            # Add similarty property to the item based on price deviation and similarty of name
            for item in item_list:
                item.similarty = find_similarty(item, Item(name=name,price=float(price), description=description))
                
            # Sort the list 
            item_list.sort(key=lambda x: x.similarty, reverse=True) # type: ignore

            # Create table headers and a list for the table's data
            table_headers = ['name', 'price','match', 'urls']
            table_data = []
            
            
            # Add items to the table 
            for index,item in enumerate(item_list):
                if index >= count:
                    break
                table_data.append((item.name,str(item.price) + "$",str(round(item.similarty,1)) + '%', item.url))
            
            # Print the table and the highest match 
            click.echo(tabulate.tabulate(tabular_data=table_data, headers=table_headers, tablefmt='fancy_grid'))
            click.echo('-----highest match-----')
            if len(item_list):
                click.echo(f'{item_list[0].name} - {str(item_list[0].price) + "$"} - {item_list[0].url}')
            else: 
                click.echo('no items were found')
            
        else:
            click.echo(f'Ivory failed (status_code returned {res.status_code})')
        
    except TimeoutError:
        click.echo(f'Ivory request timeouted')

    

def find_similarty(item_found : Item, item_given : Item) -> int:
    """_summary_

    Args:
        item (Item): _description_

    Returns:
        int: _description_
    """

    name_similarity = fuzz.ratio(item_found.name, item_given.name)
    description_similarity = fuzz.ratio(item_found.description, item_given.description)
    
    if item_given.price is None:
        return (name_similarity + description_similarity) / 2 

    price_similarty = round(abs((item_given.price - item_found.price) / item_given.price) * 100) * 0.5
    
    return (name_similarity * 5 + description_similarity * 1 - price_similarty * 0.025) / 3
    
    
    
    

if __name__=='__main__':
    cli()
    
    

