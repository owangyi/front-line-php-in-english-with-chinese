# CHAPTER 14

## COLLECTIONS While this book isn't meant to discuss every pattern you could think of, I find that a few are worth mentioning. That's why I'm also spending a chapter on collections: an alternative way of dealing with lists. We covered the built-in array functionality PHP has to offer and object-oriented programming, so collections that are a more functional way of solving problems fit well with these topics.

Maybe you haven't heard of collections before, so let's explain what they are first.

The core value of collections is that they allow for a more declarative programming style instead of an imperative one. The difference? An imperative programming style uses code to describe how something should be done; a declarative style describes the expected result.

Let's explain the difference further with an example. One of the best examples of a declarative language is SQL:

```php
SELECT id, number FROM invoices WHERE invoice_date BETWEEN "2020-01-01" AND "2020-01-31";

```

An SQL query doesn't specify how data should be retrieved from a database, rather it describes what the expected result should be. In fact, SQL servers could apply differ -

ent kinds of algorithms to solve the same query.Compare the declarative style with an imperative one in PHP:

```php
$invoicesForJanuary = [];

foreach ($allInvoices as $invoice) {

    if (
$invoice=>paymentDate=>between(

            new DateTimeImmutable('2020-01-01'), 

            new DateTimeImmutable('2020-01-31')

```

        )

```php
    ) {
$invoicesForJanuary[] = [$invoice=>id, $invoice=>number];

    }

}

```

Our PHP implementation is more cluttered because it's concerned with the technical details of looping over a list of items and how filtering them should be done.

Collections aim to provide a more declarative interface. Here's what it'd look like:

```php
$invoicesForJanuary = $allInvoices

```

    =>filter(fn (Invoice $invoice): bool => 

```php
$invoice=>paymentDate=>between(

            new DateTimeImmutable('2020-01-01'), 

            new DateTimeImmutable('2020-01-31')

```

        )

    )

    =>map(fn (Invoice $invoice): array => 

        [$invoice=>id, $invoice=>number]

    )   

A collection represents what would otherwise be a normal array, and provides lots of methods that have a more declarative approach. There's:

• filter  to filter out results,

• reject  being the counterpart of filter ,

• map which transforms each item in the collection to something else,

• reduce  which reduces to whole collection to a single result; and there's lots more.

You might get a functional programming vibe right now with functions such as filter , 

map and reduce . Collections do indeed find much of their inspiration in functional programming, but there are significant differences to real functional programming still: there's no guarantee our functions are pure, you can't compose functions out of others, and currying isn't really relevant in the context of collections. So while the col -

lections API does have some similarities with functional programming, there also are significant differences.Doing a deep dive in functional programming is outside this book's scope, especially since PHP isn't the best language to write real functional code with. I can highly rec -

ommend the book "Thinking Functionally in PHP" by Larry Garfield if you want to know more. In the book, Larry explains the core ideas of functional programming in the language you're familiar with. He also explains why you shouldn't use the approach in production PHP applications, but it's a great way to learn the functional programming concepts within a familiar language.

When you start thinking in collections, you'll start noticing many places in your code with loops or conditionals that could be refactored to collections. Refactoring to a declarative style can indeed make code easier to read and understand - an invaluable asset if you're working in large and complex code bases. Another book I'd highly rec -

ommend is called "Refactoring to Collections" By Adam Wathan (https://adamwathan.

me/refactoring-to-collections/ ). In it Adam describes the ideas of collection more in depth: he explains all the building blocks needed to build collections, and gives lots of examples of using collections in the wild.

If you're looking for a production-ready implementation of collections, I'd highly rec -

ommend using illuminate/collection , which is the implementation also used by Laravel. Besides being thorough and robust implementation, it's also very well documented: https://laravel.com/docs/8.x/collections .
