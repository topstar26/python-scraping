from bs4 import BeautifulSoup
import requests
import csv

source = requests.get('http://192.168.0.12:10086/blogs').text
soup = BeautifulSoup(source, 'lxml')

csv_file = open('site_blog.csv', 'w', encoding='UTF-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['title', 'author', 'blog_url', 'summary'])
post = soup.find('ul', class_="blogs_browse" )
for article in post.find_all('li'):
    # print(article.prettify())
    title = article.find('span', class_='blogs_browse_info_title')
    title = title.h3.a.text
    print (title)

    try:
        url = article.find('div', class_='blogs_browse_photo')
        url = url.a['href']
        blog_url = f'http://192.168.0.12:10086{url}'
    except Exception as e:
        blog_url = None

    print(blog_url)

    author = article.find('p', class_='blogs_browse_info_date')
    author = author.a.text
    print(author)

    summary = article.find('p', class_='blogs_browse_info_blurb').text
    print(summary)

    print()
    csv_writer.writerow([title, author, blog_url, summary])

csv_file.close()