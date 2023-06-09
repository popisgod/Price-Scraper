# Standard library imports
import re 
from dataclasses import dataclass
from typing import Tuple, List


# Third party imports
import bs4 
import click
import requests
import tabulate 
from fuzzywuzzy import fuzz
from deep_translator import GoogleTranslator

# Local application imports


# Scraped websites 
KSP = 'https://ksp.co.il/web/cat/'
IVORY = 'https://www.ivory.co.il/catalog.php'
TMS = 'https://tms.co.il/'
TRANSLATOR = GoogleTranslator(source='auto', target='en')

@dataclass 
class Item: 
    name: str
    price : int 
    similarty : int | None = None
    url : str | None = None

@click.group()
def cli():
    pass


@cli.command(name='ivory')
@click.argument('name')
@click.option('--description', default=None, help='Optional description of the product', type=str)
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

 
            item_list : List[Item] = []
            for index in range(len(name_elements)):
                item_name = TRANSLATOR.translate(name_elements[index].text.strip())
                item_price = int(price_elements[index].text.strip())
                item_list.append(Item(name=item_name, price=item_price))

            # Add similarty property to the item based on price deviation and similarty of name
            for item in item_list:
                item.similarty = find_similarty(item, Item(name=name + description,price=price))
                
            # Sort the list 
            item_list.sort(key=lambda x: x.similarty, reverse=True) # type: ignore

            # Create table headers and a list for the table's data
            table_headers = ['name', 'price','match']
            table_data = []
            
            
            # Add items to the table 
            for index,item in enumerate(item_list):
                if index >= count:
                    break
                table_data.append((item.name,str(item.price) + "$",str(item.similarty) + '%'))
            
            # Print the table and the highest match 
            click.echo(tabulate.tabulate(tabular_data=table_data, headers=table_headers, tablefmt='fancy_grid'))
            click.echo('-----highest match-----')
            click.echo(f'{item_list[0].name} - {str(item_list[0].price) + "$"}')
            
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
    
    if item_given.price is None:
        return name_similarity
    
    price_similarty = round(abs((item_given.price - item_found.price) / item_given.price) * 100)
    
    return round(name_similarity - price_similarty*0.40)
    
    
    
    

if __name__=='__main__':
    cli()
    
    

