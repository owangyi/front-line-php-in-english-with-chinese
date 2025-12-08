# 第十四章

## 集合

虽然这本书不打算讨论你能想到的每一种模式，但我发现有一些值得提及。这就是为什么我也花一章来讨论集合：处理列表的另一种方式。我们涵盖了 PHP 必须提供的内置数组功能和面向对象编程，所以集合是一种更函数式的问题解决方法，与这些主题很好地契合。

也许你以前没有听说过集合，所以让我们先解释一下它们是什么。

集合的核心价值是它们允许更声明式的编程风格，而不是命令式的。区别是什么？命令式编程风格使用代码来描述应该如何做某事；声明式风格描述预期的结果。

让我们用一个例子进一步解释区别。声明式语言的最佳例子之一是 SQL：

```php
SELECT id, number FROM invoices WHERE invoice_date BETWEEN "2020-01-01" AND "2020-01-31";

```

SQL 查询不指定如何从数据库中检索数据，而是描述预期的结果应该是什么。事实上，SQL 服务器可以应用不同

的算法来解决相同的查询。

将声明式风格与 PHP 中的命令式风格进行比较：

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

我们的 PHP 实现更加混乱，因为它关注循环遍历项目列表和如何过滤它们的技术细节。

集合旨在提供更声明式的接口。以下是它的样子：

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

集合表示原本是普通数组的东西，并提供许多具有更声明式方法的方法。有：

• filter 来过滤结果，

• reject 是 filter 的对应物，

• map 将集合中的每个项目转换为其他东西，

• reduce 将整个集合减少为单个结果；还有很多。

你现在可能会从 filter、map 和 reduce 等函数中获得函数式编程的感觉。集合确实在函数式编程中找到了很多灵感，但与真正的函数式编程仍有显著差异：不能保证我们的函数是纯的，你不能从其他函数组合函数，柯里化在集合的上下文中并不真正相关。所以虽然集合 API 确实与函数式编程有一些相似之处，但也有显著差异。深入探讨函数式编程超出了本书的范围，特别是因为 PHP 不是编写真正的函数式代码的最佳语言。如果你想知道更多，我可以强烈推荐 Larry Garfield 的书"Thinking Functionally in PHP"。在书中，Larry 用你熟悉的语言解释了函数式编程的核心思想。他还解释了为什么你不应该在 PHP 生产应用程序中使用这种方法，但这是在熟悉语言中学习函数式编程概念的绝佳方式。

当你开始用集合思考时，你会开始注意到代码中许多带有循环或条件的地方可以重构为集合。重构为声明式风格确实可以使代码更容易阅读和理解——如果你在大型和复杂的代码库中工作，这是一笔宝贵的财富。我强烈推荐的另一本书是 Adam Wathan 的"Refactoring to Collections"（https://adamwathan.me/refactoring-to-collections/）。在其中，Adam 更深入地描述了集合的思想：他解释了构建集合所需的所有构建块，并提供了许多在现实中使用集合的例子。

如果你正在寻找一个可用于生产的集合实现，我强烈推荐使用 illuminate/collection，这也是 Laravel 使用的实现。除了是一个彻底和健壮的实现之外，它也有很好的文档：https://laravel.com/docs/8.x/collections。

