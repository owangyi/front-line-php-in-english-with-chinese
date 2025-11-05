# Chapter 8: Short Closures

Some might consider them long overdue, but they are finally supported since PHP 7.4:

有些人可能认为它们早就该有了，但自 PHP 7.4 起终于支持了：短闭包。不用再写像传递给 `array_map` 回调这样的闭包：

short closures. Instead of writing closures like the one passed as an array_map call-

你可以用简短的形式写它们：

back:

短闭包与普通闭包有两个主要区别：

$itemPrices = array_map(

- 它们只支持一个表达式，该表达式也是返回语句
- 它们不需要 `use` 语句来访问外部作用域的变量

function (OrderLine $orderLine) {

在其他方面，它们的行为与普通闭包相同：它们支持引用、参数展开、类型提示、返回类型……说到类型，你可以用更严格类型化的方式重写前面的示例：

return $orderLine=>item=>price;

还有一件事，引用也是允许的，既适用于参数，也适用于返回值。如果你想通过引用返回一个值，应该使用以下语法：

},

你可能已经注意到了：短闭包只能有一个表达式；它可能为了格式化而跨越多行，但必须始终是一个表达式。原因如下：短闭包的目标是减少冗长。`fn` 当然在所有情况下都比 `function` 短。然而，有人认为如果你要处理多行函数，使用短闭包的好处就少了。毕竟，多行闭包根据定义已经更冗长了；所以能够跳过两个关键字（`function` 和 `return`）不会有太大区别。

$order=>lines

虽然我能想到我的项目中有很多单行闭包，但也有大量的多行闭包，我承认在这些情况下缺少短语法。不过，有希望：将来可能会添加多行短闭包，但我们还需要再等一段时间。

);

短闭包和普通闭包之间的另一个重要区别是，短闭包不需要 `use` 关键字就能访问外部作用域的数据：

You can write them in a short form:

重要的是要注意，你无法修改外部作用域的变量：它们按值绑定，而不是按引用绑定，除非你处理的是始终按引用传递的对象。顺便说一下，这是对象在任何地方（不仅仅是短闭包中）的默认行为。

$itemPrices = array_map(

一个例外当然是 `$this` 关键字，它的行为与普通闭包完全相同：

fn ($orderLine) => $orderLine=>item=>price,

说到 `$this`，你可以将短闭包声明为静态，这意味着你无法在其中访问 `$this`：

$order=>lines

关于短闭包，目前就这些了。你可以想象还有改进的空间。人们一直在讨论多行短闭包以及能够在类方法中使用该语法。我们将不得不等待未来版本，看看短闭包是否会以及如何发展。

);

Short closures differ from normal closures in two ways:

•  they only support one expression, and that's also the return statement; and

•  they don't need a use statement to access variables from the outer scope.

96

Concerning everything else, they act like a normal closure would: they support refer-

ences, argument spreading, type hints, return types… Speaking of types, you could

rewrite the previous example in more strictly typed way, like so:

$itemPrices = array_map(

fn (OrderLine $orderLine): int => $orderLine=>item=>price,

$order=>lines

);

One more thing, references are also allowed, both for the arguments as well as the

return values. If you want to return a value by reference, the following syntax should

be used:

fn&($x) => $x

No Multi-Line

You might have noticed it already: short closures can only have one expression; it

may be spread over multiple lines for formatting, but it must always be one expres-

sion. The reasoning is as follows: the goal of short closures is to reduce verbosity. fn

is of course shorter than function in all cases. However, it was argued that if you're

dealing with multi-line functions, there is less to be gained by using short closures.

After all, multi-line closures are by definition already more verbose; so being able to

skip two keywords (function and return) wouldn't make much of a difference.

While I can think of many one-line closures in my projects, there are also plenty of

multi-line ones, and I admit to missing the short syntax in those cases. There's hope,

though: it will be possible to add multi-line short closures in the future, but we'll have

to wait still a little longer.

Chapter 08 - Short Closures

Values from Outer Scope

Another significant difference between short and normal closures is that the short

ones don't require the use keyword to be able to access data from the outer scope:

$modifier = 5;

array_map(fn ($x) => $x * $modifier, $numbers);

It's important to note that you won't be able to modify variables from that outer scope:

they are bound by value and not by reference, that is unless you're dealing with

objects that are always passed by reference. That's the default behaviour for objects

everywhere, by the way, not just in short closures.

One exception is of course the $this keyword, which acts exactly the same as normal

closures:

array_map(fn ($x) => $x * $this=>modifier, $numbers);

Speaking of $this, you can declare a short closure to be static, which means you

won't be able to access $this from within it:

static fn ($x) => $x * $this=>modifier;

// Fatal error: Uncaught Error: Using $this when not in object context

That's about all there is to say about short closures for now. You can imagine there's

room for improvement. People have been talking about multi-line short closures and

being able to use the syntax for class methods. We'll have to wait for future versions

to see whether and how short closures will evolve.

98

