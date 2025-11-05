# Chapter 14: Collections

While this book isn't meant to discuss every pattern you could think of, I find that a

虽然这本书的目的不是讨论你能想到的每一个模式，但我发现有一些值得提及。这就是为什么我也花一章来讨论集合：处理列表的另一种方式。我们已经涵盖了 PHP 提供的内置数组功能和面向对象编程，所以集合是一种更函数式的问题解决方法，与这些主题很好地契合。

few are worth mentioning. That's why I'm also spending a chapter on collections: an

也许你以前没有听说过集合，所以让我们先解释一下它们是什么。

alternative way of dealing with lists. We covered the built-in array functionality PHP

集合的核心价值是它们允许更声明式的编程风格，而不是命令式的。区别是什么？命令式编程风格使用代码来描述如何完成某事；声明式风格描述预期的结果。

has to offer and object-oriented programming, so collections that are a more function-

让我们用一个例子进一步解释差异。声明式语言的最佳例子之一是 SQL：

al way of solving problems fit well with these topics.

SQL 查询不指定如何从数据库中检索数据，而是描述预期的结果应该是什么。事实上，SQL 服务器可以应用不同类型的算法来解决相同的查询。

Maybe you haven't heard of collections before, so let's explain what they are first.

将声明式风格与 PHP 中的命令式风格进行比较：

The core value of collections is that they allow for a more declarative programming

我们的 PHP 实现更加混乱，因为它关注循环遍历项目列表的技术细节以及如何过滤它们。

style instead of an imperative one. The difference? An imperative programming style

集合旨在提供更声明式的接口。这是它的样子：

uses code to describe how something should be done; a declarative style describes

集合表示原本是普通数组的东西，并提供许多具有更声明式方法的方法。有：

the expected result.

- `filter` 用于过滤结果
- `reject` 是 `filter` 的对立面
- `map` 将集合中的每个项目转换为其他东西
- `reduce` 将整个集合减少为单个结果；还有很多。

Let's explain the difference further with an example. One of the best examples of a

你可能现在会从 `filter`、`map` 和 `reduce` 等函数中获得函数式编程的感觉。集合确实在函数式编程中找到了很多灵感，但与真正的函数式编程仍有显著差异：不能保证我们的函数是纯的，你不能从其他函数组合函数，并且在集合的上下文中柯里化并不真正相关。所以虽然集合 API 确实与函数式编程有一些相似之处，但也有显著差异。

declarative language is SQL:

深入探讨函数式编程超出了本书的范围，特别是因为 PHP 不是编写真正函数式代码的最佳语言。如果你想了解更多，我强烈推荐 Larry Garfield 的《Thinking Functionally in PHP》一书。在书中，Larry 用你熟悉的语言解释了函数式编程的核心思想。他还解释了为什么你不应该在生产 PHP 应用程序中使用这种方法，但这是在熟悉语言中学习函数式编程概念的好方法。

SELECT id, number

当你开始用集合思考时，你会开始注意到代码中许多有循环或条件的地方可以重构为集合。重构为声明式风格确实可以使代码更容易阅读和理解——如果你在大型和复杂的代码库中工作，这是一笔宝贵的资产。我强烈推荐的另一本书是 Adam Wathan 的《Refactoring to Collections》（https://adamwathan.me/refactoring-to-collections/）。在其中，Adam 更深入地描述了集合的思想：他解释了构建集合所需的所有构建块，并提供了大量在现实中使用集合的例子。

FROM invoices

如果你正在寻找一个可用于生产的集合实现，我强烈推荐使用 `illuminate/collection`，这也是 Laravel 使用的实现。除了是一个彻底和健壮的实现之外，它也有很好的文档：https://laravel.com/docs/8.x/collections。

WHERE invoice_date BETWEEN "2020-01-01" AND "2020-01-31";

An SQL query doesn't specify how data should be retrieved from a database, rather it

describes what the expected result should be. In fact, SQL servers could apply differ-

ent kinds of algorithms to solve the same query.

168

Compare the declarative style with an imperative one in PHP:

$invoicesForJanuary = [];

foreach ($allInvoices as $invoice) {

if (

$invoice=>paymentDate=>between(

new DateTimeImmutable('2020-01-01'),

new DateTimeImmutable('2020-01-31')

)

) {

$invoicesForJanuary[] = [$invoice=>id, $invoice=>number];

}

}

Our PHP implementation is more cluttered because it's concerned with the technical

details of looping over a list of items and how filtering them should be done.

Chapter 14 - Collections

Collections aim to provide a more declarative interface. Here's what it'd look like:

$invoicesForJanuary = $allInvoices

=>filter(fn (Invoice $invoice): bool =>

$invoice=>paymentDate=>between(

new DateTimeImmutable('2020-01-01'),

new DateTimeImmutable('2020-01-31')

)

)

=>map(fn (Invoice $invoice): array =>

[$invoice=>id, $invoice=>number]

)

A collection represents what would otherwise be a normal array, and provides lots of

methods that have a more declarative approach. There's:

•  filter to filter out results,

•  reject being the counterpart of filter,

•  map which transforms each item in the collection to something else,

•  reduce which reduces to whole collection to a single result; and there's lots

more.

You might get a functional programming vibe right now with functions such as filter,

map and reduce. Collections do indeed find much of their inspiration in functional

programming, but there are significant differences to real functional programming

still: there's no guarantee our functions are pure, you can't compose functions out of

others, and currying isn't really relevant in the context of collections. So while the col-

lections API does have some similarities with functional programming, there also are

significant differences.

170

Doing a deep dive in functional programming is outside this book's scope, especially

since PHP isn't the best language to write real functional code with. I can highly rec-

ommend the book "Thinking Functionally in PHP" by Larry Garfield if you want to know

more. In the book, Larry explains the core ideas of functional programming in the

language you're familiar with. He also explains why you shouldn't use the approach in

production PHP applications, but it's a great way to learn the functional programming

concepts within a familiar language.

When you start thinking in collections, you'll start noticing many places in your code

with loops or conditionals that could be refactored to collections. Refactoring to a

declarative style can indeed make code easier to read and understand - an invaluable

asset if you're working in large and complex code bases. Another book I'd highly rec-

ommend is called "Refactoring to Collections" By Adam Wathan (https://adamwathan.

me/refactoring-to-collections/). In it Adam describes the ideas of collection more in

depth: he explains all the building blocks needed to build collections, and gives lots of

examples of using collections in the wild.

If you're looking for a production-ready implementation of collections, I'd highly rec-

ommend using illuminate/collection, which is the implementation also used by

Laravel. Besides being thorough and robust implementation, it's also very well docu-

mented: https://laravel.com/docs/8.x/collections.

