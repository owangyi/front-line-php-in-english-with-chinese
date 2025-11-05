# Chapter 10: Match

PHP 8 introduced the new match expression - a powerful feature that will often be the

PHP 8 引入了新的 match 表达式——一个强大的功能，通常比使用 switch 更好的选择。我说"通常"是因为 match 和 switch 都有对方无法覆盖的特定用例。那么到底有什么区别？让我们通过比较两者来开始。以下是一个经典的 switch 示例：

better choice compared to using switch. I say "often" because both match and switch

这是它的 match 等效写法：

also have specific use cases that aren't covered by the other. So what exactly are the

首先，match 表达式明显更短：

differences? Let's start by comparing the two. Here's a classic switch example:

- 它不需要 break 语句
- 它可以使用逗号将不同的分支合并为一个
- 它返回一个值，所以你只需要赋值一次

switch ($statusCode) {

所以从语法角度来看，match 总是更容易编写。但还有更多差异。

case 200:

我称 match 为表达式，而 switch 是语句。两者之间确实有区别。表达式组合值和函数调用，并被解释为一个新值。换句话说：它返回一个结果。这就是为什么我们可以将 match 的结果存储到变量中，而 switch 不可能做到这一点。

case 300:

match 会进行严格的类型检查，而不是宽松的。就像使用 `===` 而不是 `==`。然而，可能有一些情况下你希望 PHP 自动转换变量的类型，这就解释了为什么你不能用 match 替换所有 switch。

$message = null;

当没有 default 分支且值不匹配任何给定选项时，PHP 会在运行时抛出 `UnhandledMatchError`。再次强调严格性，但这将防止细微的错误被忽视。

break;

就像短闭包一样，你只能写一个表达式。表达式块可能会在某个时候添加，但还不清楚具体什么时候。

case 400:

我已经提到了缺少 break；这也意味着 match 不允许 fallthrough 条件，就像第一个 switch 示例中的两个合并的 case 行一样。但另一方面，你可以在同一行上组合条件，用逗号分隔：

$message = 'not found';

当 match RFC 被讨论时，一些人建议没有必要添加它，因为不使用额外关键字而是依赖数组键已经可以实现相同的功能。以下是我们想要基于更复杂的正则搜索匹配值的示例。在这里，我们使用一些人提到的作为 match 替代方案的数组符号：

break;

但有一个重要的警告：这种技术会先执行所有正则函数来构建数组。另一方面，match 会逐个分支评估，这是更优的方法。

case 500:

最后，由于 PHP 8 中的 throw 表达式，也可以直接从分支中抛出，如果你愿意的话：

$message = 'server error';

还有一个重要的功能缺失：适当的模式匹配。这是一种在其他编程语言中使用的技术，允许复杂的匹配规则而不是简单的比较。把它想象成正则表达式，但是针对变量而不是文本。

break;

模式匹配目前还不支持，因为它是一个相当复杂的功能。不过，它已被提及作为 match 的未来改进。我已经在期待它了！

default:

如果我需要用一句话总结 match 表达式，我会说它是更严格、更现代的小兄弟 switch 的版本。

$message = 'unknown status code';

有一些情况——看到我做了什么吗？——switch 会提供更多的灵活性，特别是在多行代码块和类型转换方面。另一方面，我发现 match 的严格性很有吸引力，模式匹配的前景将是 PHP 的一个改变游戏规则的功能。

break;

我承认我过去从未写过 switch 语句，因为它的许多怪癖；这些怪癖实际上 match 都解决了。所以虽然它还不完美，但有一些用例 match 会是一个很好的…匹配。

}

---

108

And here is its match equivalent:

$message = match ($statusCode) {

200, 300 => null,

400 => 'not found',

500 => 'server error',

default => 'unknown status code',

};

First of all, the match expression is significantly shorter:

•

•

•

it doesn't require a break statement;

it can combine different arms into one using a comma; and

it returns a value, so you only have to assign the result once.

So from a syntactical point of view, match is always easier to write. There are more dif-

ferences, though.

Expression or Statement?

I've called match an expression, while switch is a statement. There's indeed a

difference between the two. An expression combines values and function calls,

and is interpreted to a new value. In other words: it returns a result. This is why

we can store the result of match into a variable, while that isn't possible with

switch.

Chapter 10 - Match

No Type Coercion

match will do strict type checks instead of loose ones. It's like using === instead of ==.

However, there might be cases where you want PHP to automatically juggle a vari-

able's type, which explains why you can't replace all switches with matches.

$statusCode = '200';

$message = match ($statusCode) {

200 => null

default => 'Unknown status code',

};

// $message = 'Unknown status code'

Unknown values cause an error

When there's no default arm and when a value comes in that doesn't match any given

option, PHP will throw an UnhandledMatchError at runtime. Again more strictness, but

it will prevent subtle bugs from going unnoticed.

$statusCode = 400;

$message = match ($statusCode) {

200 => 'perfect',

};

// UnhandledMatchError

110

Only Single-Line Expressions, For Now

Just like short closures, you can only write one expression. Expression blocks will

probably get added at one point, but it's still not clear when exactly.

Combining Conditions

I already mentioned the lack of break; this also means that match doesn't allow for

fallthrough conditions, like the two combined case lines in the first switch example.

On the other hand though, you can combine conditions on the same line, separated

by commas:

$message = match ($statusCode) {

200, 300, 301, 302 => 'combined expressions',

};

Complex Conditions and Performance

When the match RFC was being discussed, some people suggested it wasn't nec-

essary to add it, since the same was already possible without additional keywords

but instead relying on array keys. Take this example where we want to match a value

Chapter 10 - Match

based on a more complex regex search. In here we're using the array notation some

people mentioned as an alternative to match:

$message = [

$this=>matchesRegex($line) => 'match A',

$this=>matchesOtherRegex($line) => 'match B',

][$search] =? 'no match';

But there's one big caveat: this technique will execute all regex functions first to

build the array. match, on the other hand, will evaluate arm by arm, which is the more

optimal approach.

Throwing Exceptions

Finally, because of throw expressions in PHP 8, it's also possible to directly throw from

an arm, if you'd like to.

$message = match ($statusCode) {

200 => null,

500 => throw new ServerError(),

default => 'unknown status code',

};

112

Pattern Matching

There's one important feature still missing: proper pattern matching. It's a technique

used in other programming languages to allow for intricate matching rules rather than

simple comparisons. Think of it as regex, but for variables instead of text.

Pattern matching isn't supported right now because it's quite a complex feature. It

has been mentioned as a future improvement for match though. I'm already looking

forward to it!

So, Switch or Match?

If I'd need to summarise the match expression in one sentence, I'd say it's the stricter

and more modern version of it's little switch brother.

There are some cases — see what I did there? — where switch will offer more flexibil-

ity, especially with multiline code blocks and its type juggling. On the other hand, I find

the strictness of match appealing, and the perspective of pattern matching would be a

game-changer for PHP.

I admit I never wrote a switch statement in the past because of its many quirks; quirks

that match actually solves. So while it's not perfect yet, there are use cases where

match would be a good… match.

Chapter 10 - Match

PART II

Building With PHP

