class Article:
    all = []  # Class-level attribute to track all created Article instances

    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        self.title = title
        Article.all.append(self)  # Append the new Article instance to the all list

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = self.validate_title(title)

    @staticmethod
    def validate_title(title):
        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if len(title) < 5 or len(title) > 50:
            raise ValueError("Title must be between 5 and 50 characters")
        return title

class Author:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if hasattr(self, '_name'):
            raise AttributeError("Cannot modify name after it is set")
        self._name = self.validate_name(name)

    @staticmethod
    def validate_name(name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if len(name) < 1:
            raise ValueError("Name must be longer than 0 characters")
        return name

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list(set(article.magazine for article in self.articles()))

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        topics = list(set(magazine.category for magazine in self.magazines()))
        return topics if topics else None

class Magazine:
    all_magazines = []  # Class-level attribute to track all created Magazine instances

    def __init__(self, name, category):
        self.name = name
        self.category = category
        Magazine.all_magazines.append(self)  # Append the new Magazine instance to the all_magazines list

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = self.validate_magazine_name(name)

    @staticmethod
    def validate_magazine_name(name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if len(name) < 2 or len(name) > 16:
            raise ValueError("Name must be between 2 and 16 characters, inclusive")
        return name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if not isinstance(category, str):
            raise ValueError("Category must be a string")
        if len(category) == 0:
            raise ValueError("Category must have length greater than 0")
        self._category = category

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list(set(article.author for article in self.articles()))

    def article_titles(self):
        titles = [article.title for article in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        author_count = {author: 0 for author in self.contributors()}
        for article in self.articles():
            author_count[article.author] += 1
        return [author for author, count in author_count.items() if count > 2] or None

    @classmethod
    def top_publisher(cls):
        if not cls.all_magazines:
            return None
        return max(cls.all_magazines, key=lambda mag: len(mag.articles()), default=None)