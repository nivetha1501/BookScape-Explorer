import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database Configuration
DB_CONFIG = {
    "user": "root",
    "password": "nivi",
    "host": "localhost",
    "port": "3306",  
    "database": "books_1"
}

# Create a SQLAlchemy engine using PyMySQL
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
engine = create_engine(DATABASE_URL)

# Inject CSS for a complete background change
st.markdown(
    """
 
    <style>
    /* Change the background color */
    .stApp {
        background-color:rgb(183, 197, 184); /* Light grayish-blue */
    }
    </style>
    
    """,
    unsafe_allow_html=True
)

# Function to run queries safely
def run_query(query, params=None):
    try:
        return pd.read_sql(query, engine, params=params)
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame()


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

    .custom-title-1 {
        font-family: 'Great Vibes', cursive;
        font-size: 70px;
        color:rgb(59, 27, 238); /* White text */
        text-align: center;
        text-shadow: 2px 2px 4px #000000; /* Black shadow */
        padding: 10px;
        background: linear-gradient(90deg,rgb(232, 230, 238) ,rgb(244, 227, 227)); /* Gradient background */
        border-radius: 10px;
    }
    </style>
    <h1 class="custom-title-1">BookScape Explorer</h1>
    """,
    unsafe_allow_html=True
)




# Using columns instead of sidebar
col1, col2 = st.columns(2)

# Column 1: Year Filter
with col1:
    year = st.text_input("Enter year:")
    if year:
        try:
            year = int(year)
            if 1000 <= year <= 9999:
                st.write(f"You entered the year: {year}")
            else:
                st.error("Please enter a valid year between 1000 and 9999.")
        except ValueError:
            st.error("Please enter a numeric value for the year.")


# Column 2: Keyword Search Filter
    with col2:
        keyword = st.text_input("Enter your keyword:")

    # Build the query conditionally based on input
    query = """
    SELECT DISTINCT book_title, book_authors, year
    FROM project_2
    WHERE 1=1
    """
    params = []

    # Add keyword filter if provided
    if keyword:
        query += " AND book_title LIKE %s"
        params.append(f"%{keyword}%")

    # Add year filter if provided
    if year:
        query += " AND year = %s"
        params.append(year)

    # Only run the query if there's at least one filter applied
    if params:
        try:
            result = run_query(query, tuple(params))  # Convert params to tuple safely

            # Handle missing or empty authors by replacing them with 'Unknown'
            result['book_authors'] = result['book_authors'].fillna('Unknown')  # Replace NULL with 'Unknown'
            result['book_authors'] = result['book_authors'].replace('', 'Unknown')  # Replace empty string with 'Unknown'

            # Handle missing or invalid year by replacing them with 'Unknown Year'
            result['year'] = result['year'].fillna('Unknown')  # Replace NULL year with 'Unknown Year'
            result['year'] = result['year'].replace('', 'Unknown')  # Replace empty string with 'Unknown Year'

            # Remove duplicate book titles if any remain
            if not result.empty:
                result = result.drop_duplicates(subset=['book_title'])

                st.write("📚 Books matching your criteria:")
                st.dataframe(result)  # Display results in a table
            else:
                st.write("❌ No books found with the given keyword and year.")

        except Exception as e:
            st.error(f"Database query failed: {e}")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap'); /* Import new font */

    .custom-title-2 {
        font-family: 'Poppins', sans-serif; /* Use the new font */
        font-size: 30px;
        color: #ffffff; /* White text */
        text-align: center;
        text-shadow: 2px 2px 4px #000000; /* Black shadow */
        padding: 10px;
        background: linear-gradient(90deg,rgb(227, 214, 224) ,rgb(224, 231, 221)); /* Gradient background */
        border-radius: 8px;
    }
    </style>
    <h1 class="custom-title-2">Queries</h1>
    """,
    unsafe_allow_html=True
)


# Split the queries into two columns
col_left, col_right = st.columns(2)
# First 10 queries on the left side
if st.button("Query 1"):
            st.write("Check Availability of eBooks vs Physical Books")
            query_1 = """
            select 
            sum(if(isEbook = 'yes',1,0)) as Ebook_count,
            sum(if(isEbook = 'no',0,1)) as physical_book_count
            from project_2;
            """
            result_1 = run_query(query_1)
            st.dataframe(result_1)

if st.button("Query 2"):
            st.write("Find the Publisher with the Most Books Published")
            query_2 = """
            select book_publisher,
            count(book_id) as number_of_books
            from project_2
            where book_publisher != '' and book_publisher is not null and book_publisher not in ('unknown')
            group by book_publisher
            order by number_of_books desc
            limit 1;
            """
            result_2 = run_query(query_2)
            st.dataframe(result_2)

if st.button("Query 3"):
            st.write("Identify the Publisher with the Highest Average Rating")
            query_3 = """
            select book_publisher,
            max(averageRating) as max_avg_rating
            from project_2
            where book_publisher != '' and book_publisher is not null and book_publisher not in ('unknown')
            group by book_publisher
            order by max_avg_rating desc
            limit 1;
            """
            result_3 = run_query(query_3)
            st.dataframe(result_3)

if st.button("Query 4"):
            st.write("Get the Top 5 Most Expensive Books by Retail Price")
            query_4 = """
            SELECT book_title, amount_retailPrice, currencyCode_retailPrice
            FROM project_2
            ORDER BY amount_retailPrice DESC
            LIMIT 5;
            """
            result_4 = run_query(query_4)
            st.dataframe(result_4)

if st.button("Query 5"):
            st.write("Find Books Published After 2010 with at Least 500 Pages")
            query_5 = """
            SELECT distinct book_title, book_authors, pageCount, year
            FROM project_2
            WHERE year > 2010 AND pageCount >= 500;
            """
            result_5 = run_query(query_5)
            st.dataframe(result_5)

if st.button("Query 6"):
            st.write("List Books with Discounts Greater than 20%")
            query_6 = """
            SELECT book_title, 
                amount_listPrice, 
                amount_retailPrice, 
                ((amount_listPrice - amount_retailPrice) / amount_listPrice) * 100 AS discount_percentage
            FROM project_2
            WHERE amount_listPrice > 0 AND amount_retailPrice < amount_listPrice AND 
                ((amount_listPrice - amount_retailPrice) / amount_listPrice) * 100 > 20;
            """
            result_6 = run_query(query_6)
            st.dataframe(result_6)

if st.button("Query 7"):
            st.write("Find the Average Page Count for eBooks vs Physical Books")
            query_7 = """
            SELECT isEbook, AVG(pageCount) AS avg_page_count
            FROM project_2
            GROUP BY isEbook;
            """
            result_7 = run_query(query_7)
            st.dataframe(result_7)

if st.button("Query 8"):
            st.write("Find the Top 3 Authors with the Most Books")
            query_8 = """
            select book_authors,count(book_id) as number_of_books
                from project_2
                where book_authors != '' and book_authors is not null and book_authors not in ('unknown')
                group by book_authors
                order by number_of_books desc
                limit 3;
            """
            result_8 = run_query(query_8)
            st.dataframe(result_8)

if st.button("Query 9"):
            st.write("List Publishers with More than 10 Books")
            query_9 = """
           SELECT 
                    book_publisher, 
                    COUNT(book_id) AS number_of_books 
                FROM 
                    project_2 
                WHERE 
                    TRIM(book_publisher) != '' 
                    AND book_publisher IS NOT NULL 
                    AND TRIM(LOWER(book_publisher)) NOT IN ('unknown') 
                GROUP BY 
                    book_publisher 
                HAVING 
                    COUNT(book_id) > 10;

            """
            result_9 = run_query(query_9)
            st.dataframe(result_9)

if st.button("Query 10"):
            st.write("Find the Average Page Count for Each Category")
            query_10 = """
            select categories,
            avg(pageCount) as avg_page_count
            from project_2
            where categories != '' and categories is not null and categories not in ('unknown')
            group by categories
            order by avg_page_count desc;
            """
            result_10 = run_query(query_10)
            st.dataframe(result_10)
if st.button("Query 11"):
            st.write("Retrieve Books with More than 3 Authors")
            query_11 = """
            SELECT distinct book_title, book_authors
            FROM project_2
            WHERE LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) + 1 > 3;
            """
            result_11 = run_query(query_11)
            st.dataframe(result_11)

if st.button("Query 12"):
            st.write("Books with Ratings Count Greater Than the Average")
            query_12 = """
            SELECT distinct book_title, ratingsCount
            FROM project_2
            WHERE ratingsCount > (SELECT AVG(ratingsCount) FROM project_2);
            """
            result_12 = run_query(query_12)
            st.dataframe(result_12)

if st.button("Query 13"):
            st.write("Books with the Same Author Published in the Same Year")
            query_13 = """
            SELECT DISTINCT 
                b1.book_authors,
                LEAST(b1.book_title, b2.book_title) AS book_1,
                GREATEST(b1.book_title, b2.book_title) AS book_2,
                b1.year
            FROM project_2 b1
            JOIN project_2 b2 
                ON b1.book_authors = b2.book_authors 
                AND b1.year = b2.year 
                AND b1.book_title <> b2.book_title
            WHERE b1.book_authors != '' 
                AND b1.book_authors IS NOT NULL 
                AND b1.book_authors NOT IN ('unknown')
                AND b1.year != '' 
                AND b1.year IS NOT NULL 
                AND b1.year NOT IN ('unknown')
            ORDER BY b1.book_authors, b1.year;


            """
            result_13 = run_query(query_13)
            st.dataframe(result_13)

if st.button("Query 14"):
            st.write("Books with an 'India' Keyword in the Title")
            query_14 = """
            SELECT distinct book_title, book_authors
            FROM project_2
            WHERE book_title LIKE %s;
            """
            result_14 = run_query(query_14, ('%india%',))
            st.dataframe(result_14)

if st.button("Query 15"):
            st.write("Year with the Highest Average Book Price")
            query_15 = """
            SELECT year, AVG(amount_retailPrice) AS avg_price
            FROM project_2
            GROUP BY year
            ORDER BY avg_price DESC
            LIMIT 1;
            """
            result_15 = run_query(query_15)
            st.dataframe(result_15)

if st.button("Query 16"):
            st.write("Count Authors Who Published 3 Consecutive Years")
            query_16 = """
            WITH ranked_books AS (
            SELECT book_authors, COUNT(DISTINCT year) AS consecutive_years,
           ROW_NUMBER() OVER (ORDER BY book_authors) AS row_num
            FROM project_2
            WHERE book_authors != 'Unknown'
            GROUP BY book_authors
            HAVING MAX(year) - MIN(year) >= 2
            )
            SELECT book_authors, consecutive_years
            FROM ranked_books
            WHERE row_num > 1;  
                        """
            result_16 = run_query(query_16)
            st.dataframe(result_16)

if st.button("Query 17"):
            st.write("Find authors whose Books Published in the Same Year but Under Different Publishers")
            query_17 = """
            SELECT book_authors, year, COUNT(DISTINCT book_publisher) AS publisher_count  FROM project_2  where book_authors != '' and book_authors is not null and book_authors not in ('unknown') GROUP BY book_authors, year HAVING publisher_count > 1;
            """
            result_17 = run_query(query_17)
            st.dataframe(result_17)

if st.button("Query 18"):
            st.write("Average Retail Price of eBooks and Physical Books")
            query_18 = """
            SELECT 
                AVG(CASE WHEN isEbook = TRUE THEN amount_retailPrice END) AS avg_ebook_price,
                AVG(CASE WHEN isEbook = FALSE THEN amount_retailPrice END) AS avg_physical_price
            FROM project_2;
            """
            result_18 = run_query(query_18)
            st.dataframe(result_18)

if st.button("Query 19"):
            st.write("Books with Ratings Two Standard Deviations from the Mean")
            query_19 = """
            WITH stats AS (
                SELECT AVG(averageRating) AS avg_rating, STDDEV(averageRating) AS stddev_rating
                FROM project_2
            )
            SELECT distinct book_title, averageRating, ratingsCount
            FROM project_2, stats
            WHERE averageRating > avg_rating + 2 * stddev_rating
            OR averageRating < avg_rating - 2 * stddev_rating;
            """
            result_19 = run_query(query_19)
            st.dataframe(result_19)

if st.button("Query 20"):
            st.write("Publisher with the Highest Average Rating")
            query_20 = """
            SELECT book_publisher, 
                AVG(averageRating) AS avg_rating, 
                COUNT(*) AS number_of_books_published
            FROM project_2
            where book_publisher != '' and book_publisher is not null and book_authors not in ('unknown')
            GROUP BY book_publisher
            HAVING COUNT(*) > 10
            ORDER BY avg_rating DESC
            LIMIT 1;
            """
            result_20 = run_query(query_20)
            st.dataframe(result_20)            


import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import streamlit as st
import pandas as pd

# Database setup
DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Function to fetch books from Google Books API
def fetch_books(query):
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={query}")
    response.raise_for_status()  # Raise an exception for any 4xx/5xx errors
    data = response.json()
    return data.get("items", [])

# Function to store books in the database
def store_books_in_db(books, search_key):
    session = Session()
    try:
        # Insert new books with the given search key
        for book in books:
            volume_info = book.get("volumeInfo", {})
            sale_info = book.get("saleInfo", {})

            # Handle missing or invalid values (convert to None for NULL in DB)
            book_info = {
                'book_id': book.get('id', ''),  # Book ID
                'search_key': search_key,  # The query used for the search
                'book_title': volume_info.get('title', ''),  # Book title
                'book_subtitle': volume_info.get('subtitle', ''),  # Book subtitle
                'book_authors': ", ".join(volume_info.get('authors', [])),  # Authors (comma-separated)
                'book_publisher': volume_info.get('publisher', ''),  # Publisher
                'book_description': volume_info.get('description', 'N/A'),
                'industryIdentifiers': ", ".join([identifier.get('identifier', '') for identifier in volume_info.get('industryIdentifiers', [])]),  # Industry identifiers
                'text_readingModes': volume_info.get('readingModes', {}).get('text', False),  # Text reading mode availability
                'image_readingModes': volume_info.get('readingModes', {}).get('image', False),  # Image reading mode availability
                'pageCount': volume_info.get('pageCount', None),  # Page count
                'categories': ", ".join(volume_info.get('categories', [])),  # Categories (comma-separated)
                'language': volume_info.get('language', ''),  # Language
                'imageLinks': volume_info.get('imageLinks', {}).get('thumbnail', ''),  # Thumbnail image link
                'ratingsCount': volume_info.get('ratingsCount', None),  # Ratings count (None if missing)
                'averageRating': volume_info.get('averageRating', None),  # Average rating (None if missing)
                'country': sale_info.get('country', ''),  # Sale info country
                'saleability': sale_info.get('saleability', ''),  # Saleability (e.g., if it's for sale)
                'isEbook': sale_info.get('isEbook', False),  # Is it available as an ebook?
                'amount_listPrice': sale_info.get('listPrice', {}).get('amount', None),  # List price (None if missing)
                'currencyCode_listPrice': sale_info.get('listPrice', {}).get('currencyCode', ''),  # List price currency code
                'amount_retailPrice': sale_info.get('retailPrice', {}).get('amount', None),  # Retail price (None if missing)
                'currencyCode_retailPrice': sale_info.get('retailPrice', {}).get('currencyCode', ''),  # Retail price currency code
                'buyLink': sale_info.get('buyLink', ''),  # URL to buy the book
                'year': volume_info.get('publishedDate', '').split('-')[0] if volume_info.get('publishedDate', '') else ''  # Year of publication (extracted from date)
            }

            query = text("""
                INSERT INTO project_2 (book_id, search_key, book_title, book_subtitle, book_authors, book_publisher,book_description,
                 industryIdentifiers, text_readingModes, image_readingModes, pageCount, categories, language,
                imageLinks, ratingsCount, averageRating, country, saleability, isEbook, amount_listPrice, currencyCode_listPrice,
                amount_retailPrice, currencyCode_retailPrice, buyLink, year)
                VALUES (:book_id, :search_key, :book_title, :book_subtitle, :book_authors, :book_publisher, :book_description,
                 :industryIdentifiers, :text_readingModes, :image_readingModes, :pageCount, :categories, :language,
                :imageLinks, :ratingsCount, :averageRating, :country, :saleability, :isEbook, :amount_listPrice, :currencyCode_listPrice,
                :amount_retailPrice, :currencyCode_retailPrice, :buyLink, :year)
            """)
            session.execute(query, book_info)

        session.commit()
    except Exception as e:
        st.error(f"Error saving books to the database: {e}")
    finally:
        session.close()

# Function to retrieve books from the database
def get_books_from_db(search_key=None):
    session = Session()
    try:
        if search_key:
            result = session.execute(
                text("SELECT * FROM project_2 WHERE search_key = :search_key"),
                {"search_key": search_key},
            )
        else:
            result = session.execute(text("SELECT * FROM project_2"))
        return result.fetchall()
    finally:
        session.close()

# Streamlit app
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

    .custom-title-3 {
        font-family: 'Great Vibes', cursive;
        font-size: 40px;
        color: #ffffff; /* White text */
        text-align: center;
        text-shadow: 1px 1px 3px #000000; /* Black shadow */
        padding: 10px;
        background: linear-gradient(90deg,rgb(245, 104, 104)) ,rgb(240, 21, 21)); /* Gradient background */
        border-radius: 10px;
    }
    </style>
    <h1 class="custom-title-3">Data Extraction</h1>
    """,
    unsafe_allow_html=True
)

# Input field for search query
query = st.text_input("Enter a category or keyword to fetch books:", "")

# Fetch and store books button
if st.button("Fetch and Store Books"):
    if query:
        # Fetch books from the API
        books = fetch_books(query)

        # Store books in the database
        if books:
            store_books_in_db(books, query)
            st.success(f"Books related to '{query}' have been stored in the database.")
        else:
            st.warning("No books found for the given query.")
    else:
        st.warning("Please enter a search query.")

# Display stored books button
if st.button("Display Stored Books"):
    # Retrieve books from the database
    books = get_books_from_db(search_key=query if query else None)

    # Display books as a pandas DataFrame
    if books:
        columns = ["book_id", "search_key", "book_title", "book_subtitle", "book_authors", "book_publisher",
                   "book_description", "industryIdentifiers", "text_readingModes", "image_readingModes", "pageCount", 
                   "categories", "language", "imageLinks", "ratingsCount", "averageRating", "country", "saleability", 
                   "isEbook", "amount_listPrice", "currencyCode_listPrice", "amount_retailPrice", "currencyCode_retailPrice", 
                   "buyLink", "year"]

        df_books = pd.DataFrame(books, columns=columns)
        st.dataframe(df_books)
    else:
        st.warning("No books found in the database.")