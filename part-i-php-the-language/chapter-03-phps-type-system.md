# Chapter 3: PHP's Type System

One of the most significant features of PHP 7, besides performance, is its improved

除了性能之外，PHP 7 最重要的变化之一就是类型系统的改进。严格来说，许多关键能力直到 PHP 8 才算补齐，但整体而言，这些年 PHP 的类型系统进步巨大。随着类型系统走向成熟，社区中也出现了充分利用类型信息的工程实践与工具，比如静态分析器（下一章会详细讨论其收益）。本章先聚焦于 PHP 5 到 PHP 8 期间，类型系统到底变了些什么。

type system. Granted: it took until PHP 8 before most key features were implement-

首先，引入了更多内建“标量类型”（scalar types），包括整数、字符串、布尔与浮点：

ed, but overall, PHP's type system has improved significantly over the years. With

其次（上一段示例其实已经体现了），新增了“返回类型”。在 PHP 7 之前，只能在入参上做类型约束，经常导致 docblock 与函数签名“混搭”的混乱情况；PHP 7 起可直接用返回类型将信息内嵌到签名中，既简洁又能被解释器实际检查。

its maturing type system, some community projects started to use types to their full

除参数与返回类型外，类属性也支持“类型化”（typed properties）。它们与参数/返回类似：可选、按需使用。既可以是标量类型，也可以是对象类型：

extent. Static analysers were built, which opened the doors for a whole other way

类型化属性引入了一个新的状态：未初始化（uninitialized）。以下示例中，`Money` 没有构造函数，`$amount` 未被赋值：

of programming. We'll dig deeper into the benefits of those static analysers in the

要点：

next chapter. For now, we'll focus on what exactly changed within PHP's type system

- 未初始化的类型化属性不可读取，否则致命错误；
- 由于检查发生在“访问”时，你可以持有带未初始化属性的对象；
- 允许先写后读（先赋值再读取）；
- 对类型化属性执行 `unset` 会令其回到未初始化，而非类型化属性则会变为 `null`。

between version 5 and 8.

从 PHP 7.1 起，支持可空类型（nullable types），用 `?Type` 表示。例如：

First of all, more built-in types were added: so called "scalar" types. These types are

注意，可空类型与“默认值为 null”是不同概念：可空类型依然需要传参；若希望参数可省略，需要同时提供默认值 `= null`。

integers, strings, booleans and floats:

PHP 8 引入联合类型（union types），允许返回或参数是多种类型之一，这在某些场景下能更准确表达意图；同时也新增了 `mixed` 等更宽泛的类型，用以描述“可能是任意几种常见类型之一”。

public function formatMoney(int $money): string

空值（null）在语言界有“十亿美元错误”之称，但现实中 null 在 PHP 里相当常见，于是语言也提供了更稳妥的语法来处理它，包括：

{

- 空合并运算符 `??`；
- 空合并赋值 `??=`；
- PHP 8 的 Nullsafe 运算符 `?->`，仅在目标不为 null 时才调用方法或访问属性。

// …

当然，彻底避免使用 null 也是一条路，例如“空对象模式”（Null Object Pattern）：用能代表“缺席”的对象替代 null，从而将分支逻辑收敛到多态之中。示例（保留原样）：

}

类型变体（Type Variance）是 PHP 7.4 引入的一项强大能力：允许在继承层次中“改变方法的类型签名”，但需遵循协变/逆变的规则。上面的示例中，接口声明返回 `Date`，而 `PendingInvoice` 返回 `UnknownDate` 即属于返回类型协变。

26

此外，再强调一次“可空类型 vs 默认 null”的差异：`?Type` 让值可为 null，但调用时仍需提供该参数；若要“可省略”，需再给出 `= null` 的默认值。

Next (you might have noticed this in the previous example already) return types were

本章还涵盖了更多关于 null 处理、未初始化状态、以及与向后兼容相关的小细节。随着这些能力完善，类型系统已成为现代 PHP 实践的基石之一；下一章我们将继续探讨与之相辅相成的静态分析工具链。

added. Before PHP 7 you were already able use types but only for input parameters.

This lead to a mix of doc block types and inline types — some might call it a mess:

/**

* @param \App\Offer $offer

* @param bool $sendMail

*

* @return \App\Offer

*/

public function createOffer(Offer $offer, $sendMail)

{

// …

}

Some developers who didn't want to deal with this kind of messy code chose not

to use types at all. After all, there was only a limited level of "type safety", since doc

blocks types aren't interpreted at all. Your IDE, on the other hand, would be able

to understand the doc block version, but for some people, this wasn't enough of a

benefit. As of PHP 7.0, however, the previous example could be rewritten like so:

public function createOffer(Offer $offer, bool $sendMail): Offer

{

// …

}

It's the same information, but much more concise and actually checked by the inter-

preter — we'll dive into the benefits of a type system and type safety later.

Chapter 03 - PHP's Type System

Besides parameter and return types, there are now also typed properties for classes.

Just like parameter and return types, they are opt-in; PHP won't do any type checks.

class Offer

{

public string $offerNumber;

public Money $totalPrice;

}

You can see both scalar types and objects are allowed, just like with parameter and

return types.

Now, typed properties have an interesting feature to them. Take a look at the follow-

ing example and notice that despite what you might think at first sight, it is valid and

won't throw any errors:

class Money

{

public int $amount;

}

$money = new Money();

In this example, Money doesn't have a constructor, and no value is set in its $amount

property. Even though the value of $amount isn't an integer after constructing the

28

Money object, PHP will only throw an error when we're trying to access the property,

later in the code:

var_dump($money=>amount);

// Fatal error: Typed property Money::$amount

// must not be accessed before initialization

As you can see in the error message, there's a new kind of variable state: uninitialized.

If $amount didn't have a type, its value would simply be null. Typed properties can be

nullable, so it's important to make a distinction between a type that was forgotten and

a type that's null. That's why "uninitialized" was added.

There are a few essential things to remember about uninitialized:

•  As we just saw, you cannot read from uninitialized properties; doing so will result

in a fatal error.

•  Because the uninitialized state is checked when accessing a property, you're

able to create an object with an uninitialized property.

•  You're allowed to write to an uninitialized property before reading it, which

means you could do $money=>amount = 1 after constructing it.

•  Using unset on a typed property will make it uninitialized, while unsetting an

untyped property will make it null.

•  While the uninitialized state is only checked when reading a property's value,

type validation is done when writing to it. This means that you can be sure no

invalid type will ever end up as a property's value.

I realise this behaviour might not be what you'd expect a programming language to

do. I've mentioned before that PHP tries very hard not to break backwards compat-

ibility with their updates, which sometimes results in compromises like the uninitial-

ized state. While I think that a variable's state should be checked immediately after

Chapter 03 - PHP's Type System

constructing an object, we'll have to make do with what we have. At least it's another

good reason to make use of static analysis in the next chapter.

Dealing with null

While we're on the topic of uninitialized state, let's also discuss null. Some have

called the concept of null a "billion-dollar mistake", arguing it allows for a range of

edge cases that we have to consider when writing code. It might seem strange to

work in a programming language that doesn't support null, but there are useful pat-

terns to replace it, and get rid of its pitfalls.

Let's illustrate those downsides first with an example. Here we have a Date value

object with a timestamp variable, format function and static constructor called now.

class Date

{

public int $timestamp;

public static function now(): self { /* … */ }

public function format(): string { /* … */ }

// …

}

30

Next, we have an invoice with a payment date:

class Invoice

{

public ?Date $paymentDate = null;

// …

}

The payment date is nullable because invoices can be pending and not yet have a

payment date.

As a side note: take a look at the nullable notation; I've already mentioned it but

haven't shown it until now. We've prefixed Date with a question mark, indicating that

it can either be Date or null. We've also added a default = null value, ensuring the

value is never uninitialized to prevent all those runtime errors you might encounter.

Back to our example: what if we want to do something with our payment date's time-

stamp?

$invoice=>paymentDate=>timestamp;

Since we're not sure $invoice=>paymentDate is a Date or null, we risk running into

runtime errors:

// Trying to get property 'timestamp' of non-object

Chapter 03 - PHP's Type System

Before PHP 7.0, you'd use isset to prevent those kinds of errors:

isset($invoice=>paymentDate)

? $invoice=>paymentDate=>timestamp

: null;

That's rather verbose, though, and is why a new operator was introduced: the null

coalescing operator.

$invoice=>paymentDate=>timestamp =? null;

This operator will automatically perform an isset check on its left-hand operand. If

that returns false, it will return the fallback provided by its righthand operand. In this

case, the payment date's timestamp or null. It is a nice addition that reduces the com-

plexity of our code.

PHP 7.4 added another null coalescing shorthand: the null coalescing assignment

operator. This one not only supports the default value fallback, but will also write it

directly to the left-hand operand. It looks like this:

$temporaryPaymentDate = $invoice=>paymentDate =?= Date=:now();

So if the payment date is already set, we'll use that one in $temporaryPaymentDate,

otherwise we'll use Date=:now() as the fallback for $temporaryPaymentDate and also

write it to $invoice=>paymentDate immediately.

32

A more common use case for the null coalescing assignment operator is a memoiza-

tion function: a function that stores the result once it's calculated:

function match_pattern(string $input, string $pattern) {

static $cache = [];

return $cache[$input][$pattern] =?=

(function (string $input, string $pattern) {

preg_match($pattern, $input, $matches);

return $matches[0];

})($input, $pattern);

}

Chapter 03 - PHP's Type System

This function will perform a regex match on a string with a pattern, but if the same

string and same pattern are provided, it will simply return the cached result. Before we

had the null coalescing operator assignment, we'd need to write it like so:

function match_pattern(string $input, string $pattern) {

static $cache = [];

$key = $input . $pattern;

if (! isset($cache[$key])) {

$cache[$key] = (function (string $input, string $pattern) {

preg_match($pattern, $input, $matches);

return $matches[0];

})($input, $pattern);

}

return $cache[$key];

}

There's one more null-oriented feature in PHP added in PHP 8: the nullsafe operator.

Take a look at this example:

$invoice=>paymentDate=>format();

What happens if our payment date is null? You'd again get an error:

// Call to a member function format() on null

34

Your first thought might be to use the null coalescing operator, but that wouldn't work:

$invoice=>paymentDate=>format('Y-m-d') =? null;

The null coalescing operator doesn't work with method calls on null. So before PHP

8, you'd need to do this:

$paymentDate = $invoice=>paymentDate;

$paymentDate ? $paymentDate=>format('Y-m-d') : null;

Fortunately there's the nullsafe operator which will only perform method calls when

possible and otherwise return null instead:

$invoice=>getPaymentDate()?=>format('Y-m-d');

Dealing with null — there's another way

I started this section saying null is called a "billion-dollar mistake", but next, I showed

you three ways PHP is embracing null with fancy syntax. The reality is that null is a

frequent occurrence in PHP, and it's a good thing we have syntax to deal with it in a

sane way. However, it's also good to look at alternatives to using null altogether. One

such alternative is the null object pattern.

Chapter 03 - PHP's Type System

Instead of one Invoice class that manages internal state about whether it's paid or

not; let's have two classes: PendingInvoice and PaidInvoice. The PendingInvoice

implementation looks like this:

class PendingInvoice implements Invoice

{

public function getPaymentDate(): UnknownDate

{

return new UnknownDate();

}

}

PaidInvoice looks like this:

class PaidInvoice implements Invoice

{

// …

public function getPaymentDate(): Date

{

return $this=>date;

}

}

Next, there's an Invoice interface:

interface Invoice

{

public function getPaymentDate(): Date;

}

36

Finally, here are the two date classes:

class Date

{

// …

}

class UnknownDate extends Date

{

public function format(): string

{

return '/';

}

}

The null object pattern aims to replace null with actual objects, objects that behave

differently because they represent the "absence" of the real object. Another benefit

of using this pattern is that classes become more representative of the real world:

instead of a "date or null", it's a "date or unknown date", instead of an "invoice with a

state" it's a "paid invoice or pending invoice". You wouldn't need to worry about null

anymore.

$invoice=>getPaymentDate()=>format(); // A date or '/'

You might not like this pattern, but it's important to know that the problem can be

solved this way.

Chapter 03 - PHP's Type System

Changing types

Something happened in the above code samples that I wrote down as a fact, yet it's a

significant addition to PHP's type system. We were able to change method signatures

during inheritance. Take a look at the Invoice interface:

interface Invoice

{

public function getPaymentDate(): Date;

}

It declares the return type of getPaymentDate as Date, yet we changed it in our

PendingInvoice to UnknownDate:

class PendingInvoice implements Invoice

{

public function getPaymentDate(): UnknownDate

{

/* … */

}

}

This powerful technique is called type variance; it's supported as of PHP 7.4. It's so

powerful (and a little complex) that we'll spend a whole chapter on the topic later

in this book. For now, all you need to know is that return types and input parameter

types are allowed to change during inheritance, but both have different rules to follow.

Another interesting detail has to do with nullable types. There's a difference between

a nullable type using ? and a default = null value; you've seen them used together

already in a previous example. The difference is this: if you make a type nullable in

38

PHP, you're still expected to pass something to that function; you can't just skip the

parameter:

function createOrUpdate(?Offer $offer): void

{

// …

}

createOrUpdate();

// Uncaught ArgumentCountError:

//     Too few arguments to function createOrUpdate(),

//     0 passed and exactly 1 expected

So by adding an explicit = null default value, you're allowed to omit the value alto-

gether:

function createOrUpdate(?Offer $offer = null): void

{

// …

}

createOrUpdate();

Chapter 03 - PHP's Type System

Unfortunately, because of backwards compatibility, there's a little quirk with this

system. If you assign a default = null value to a variable, it'll always be nullable. Re-

gardless of whether the type is explicitly made nullable or not, so this will be allowed:

function createOrUpdate(Offer $offer = null): void

{

// …

}

createOrUpdate(null);

Union and Other Types

There are still a few more things worth mentioning in this chapter, and the most excit-

ing one is union types. They allow you to type hint a variable with several types. Note:

the input needs to be one of those declared types. Here's an example:

interface Repository

{

public function find(int|string $id);

}

Be careful not to overuse union types, though. Too many types in the same union can

indicate that this function is trying to do too much at once.

For example: a framework might allow you to return both a Response and View object

from controller methods. Sometimes it's convenient to directly return a View, while

other times you want to have fine-grained control over the response. These are cases

where a union type on Response|View is fine. On the other hand, if you have a function

40

that accepts a union of array|Collection|string, it's probably an indication that the

function has to do too many things. It's best to think about finding a common ground

in those cases; maybe only accept Collection or array.

Finally, there are three more built-in types available.

There's the static return type available in PHP 8. It indicates that a function returns

the class where that function was called from. It differs from self since that one

always refers to the parent class, while static can also indicate the child class:

abstract class Parent

{

public static function make(): static { /* … */ }

}

class Child extends Parent { /* … */ }

$child = Child=:make();

In this example, static analysis tools and IDEs now know that $child is an instance

of Child. If self was used as a return type, they would think it was an instance of

Parent. Also note that the static keyword and static return type are two different

concepts; they just happen to have the same name (which is the case in many other

languages).

There's also the void return type added in PHP 7.1. It checks whether nothing is re-

turned from a function. Note that void cannot be combined into a union.

Finally, there's the mixed type, also available as of PHP 8. mixed

can be used to type hint "anything". It's a shorthand for the union of

array|bool|callable|int|float|null|object|resource|string. Think of mixed as

the opposite of void.

Chapter 03 - PHP's Type System

Generics and Enums

There are still two major features missing in PHP's type system today: generics and

enums. I wish I could write about them in this book, but unfortunately, they aren't sup-

ported by the language yet.

There have been efforts in the past to add both features, but there hasn't been any

consensus about how enums should be implemented, and generics would have too

large an impact on runtime performance.

This raises an interesting question: why do we need to check types at runtime? Isn't

that too late? If something goes wrong, the program crashes anyway. That's exactly

the topic we'll look at in-depth in the next chapter.

42

