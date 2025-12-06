# CHAPTER 03

## PHP'S TYPE SYSTEM
One of the most significant features of PHP 7, besides performance, is its improved type system. Granted: it took until PHP 8 before most key features were implemented, but overall, PHP's type system has improved significantly over the years. With its maturing type system, some community projects started to use types to their full extent. Static analysers were built, which opened the doors for a whole other way of programming. We'll dig deeper into the benefits of those static analysers in the next chapter. For now, we'll focus on what exactly changed within PHP's type system between version 5 and 8.

PHP 7 除了性能之外，最重要的特性之一就是改进的类型系统。诚然：直到 PHP 8 才实现了大部分关键特性，但总体而言，PHP 的类型系统在这些年有了显著改进。随着类型系统的成熟，一些社区项目开始充分利用类型。静态分析器被构建出来，这为全新的编程方式打开了大门。我们将在下一章深入探讨这些静态分析器的好处。现在，我们将专注于 PHP 5 到 8 版本之间类型系统的具体变化。

First of all, more built-in types were added: so called "scalar" types. These types are integers, strings, booleans and floats:

首先，添加了更多的内置类型：所谓的"标量"类型。这些类型包括整数、字符串、布尔值和浮点数：

```php
public function formatMoney(int $money): string
{
// …
}

```

Next (you might have noticed this in the previous example already) return types were added. Before PHP 7 you were already able use types but only for input parameters.

接下来（你可能已经在之前的例子中注意到了）添加了返回类型。在 PHP 7 之前，你已经可以使用类型，但只能用于输入参数。 

This lead to a mix of doc block types and inline types — some might call it a mess:

这导致了文档块类型和内联类型的混合——有些人可能会称之为混乱：

```php
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

```

Some developers who didn't want to deal with this kind of messy code chose not to use types at all. After all, there was only a limited level of "type safety", since doc blocks types aren't interpreted at all. Your IDE, on the other hand, would be able to understand the doc block version, but for some people, this wasn't enough of a benefit. As of PHP 7.0, however, the previous example could be rewritten like so:

一些不想处理这种混乱代码的开发者选择完全不使用类型。毕竟，只有有限的"类型安全"级别，因为文档块类型根本不会被解释。另一方面，你的 IDE 能够理解文档块版本，但对某些人来说，这还不够。然而，从 PHP 7.0 开始，之前的例子可以这样重写：

```php
public function createOffer(Offer $offer, bool $sendMail): Offer

{


    // …

}

```

It's the same information, but much more concise and actually checked by the interpreter — we'll dive into the benefits of a type system and type safety later.

这是相同的信息，但更加简洁，并且实际上会被解释器检查——我们稍后将深入探讨类型系统和类型安全的好处。

Besides parameter and return types, there are now also typed properties for classes. 

除了参数和返回类型，现在还有类的类型化属性。

Just like parameter and return types, they are opt-in; PHP won't do any type checks.

就像参数和返回类型一样，它们是可选的；PHP 不会进行任何类型检查。

```php
class Offer 

{

    public string $offerNumber;

    public Money $totalPrice;

}

```

You can see both scalar types and objects are allowed, just like with parameter and return types.

你可以看到标量类型和对象都是允许的，就像参数和返回类型一样。

Now, typed properties have an interesting feature to them. Take a look at the following example and notice that despite what you might think at first sight, it is valid and won't throw any errors:

现在，类型化属性有一个有趣的特征。看看下面的例子，注意尽管你第一眼可能不这么认为，但它是有效的，不会抛出任何错误：

```php
class Money

{

    public int $amount;

}

$money = new Money();

```

In this example, Money  doesn't have a constructor, and no value is set in its $amount property. Even though the value of $amount  isn't an integer after constructing theMoney  object, PHP will only throw an error when we're trying to access the property, later in the code:

在这个例子中，Money 没有构造函数，它的 $amount 属性也没有设置值。尽管在构造 Money 对象后，$amount 的值不是整数，PHP 只会在我们尝试访问该属性时抛出错误，稍后在代码中：

```php
var_dump($money=>amount);

// Fatal error: Typed property Money::$amount

// must not be accessed before initialization As you can see in the error message, there's a new kind of variable state: uninitialized.
```

If $amount  didn't have a type, its value would simply be null . Typed properties can be nullable, so it's important to make a distinction between a type that was forgotten and a type that's null . That's why "uninitialized" was added.

如果 $amount 没有类型，它的值将简单地是 null。类型化属性可以是可空的，因此区分被遗忘的类型和 null 类型很重要。这就是为什么添加了"未初始化"状态。

There are a few essential things to remember about uninitialized:

• As we just saw, you cannot read from uninitialized properties; doing so will result in a fatal error.

• Because the uninitialized state is checked when accessing a property, you're able to create an object with an uninitialized property.

• You're allowed to write to an uninitialized property before reading it, which means you could do $money=>amount = 1  after constructing it.

• Using unset  on a typed property will make it uninitialized, while unsetting an untyped property will make it null .

• While the uninitialized state is only checked when reading a property's value, 

type validation is done when writing to it. This means that you can be sure no invalid type will ever end up as a property's value.

关于未初始化状态，有几个重要的事情需要记住：

• 正如我们刚才看到的，你不能从未初始化的属性中读取；这样做会导致致命错误。

• 因为未初始化状态是在访问属性时检查的，所以你能够创建一个带有未初始化属性的对象。

• 允许在读取之前写入未初始化的属性，这意味着你可以在构造后执行 $money=>amount = 1。

• 对类型化属性使用 unset 会使其变为未初始化，而对非类型化属性使用 unset 会使其变为 null。

• 虽然未初始化状态只在读取属性值时检查，但类型验证在写入时进行。这意味着你可以确保无效类型永远不会成为属性的值。

I realise this behaviour might not be what you'd expect a programming language to do. I've mentioned before that PHP tries very hard not to break backwards compatibility with their updates, which sometimes results in compromises like the uninitialized state. While I think that a variable's state should be checked immediately after constructing an object, we'll have to make do with what we have. At least it's another good reason to make use of static analysis in the next chapter.

我意识到这种行为可能不是你期望编程语言会做的。我之前提到过，PHP 非常努力地不破坏向后兼容性，这有时会导致像未初始化状态这样的妥协。虽然我认为变量的状态应该在构造对象后立即检查，但我们只能接受现状。至少这是下一章使用静态分析的另一个好理由。

## Dealing with null
While we're on the topic of uninitialized state, let's also discuss null . Some have called the concept of null  a "billion-dollar mistake", arguing it allows for a range of edge cases that we have to consider when writing code. It might seem strange to work in a programming language that doesn't support null , but there are useful patterns to replace it, and get rid of its pitfalls.

当我们讨论未初始化状态时，让我们也讨论一下 null。有些人称 null 的概念为"十亿美元的错误"，认为它允许一系列我们在编写代码时必须考虑的边界情况。在一个不支持 null 的编程语言中工作可能看起来很奇怪，但有有用的模式可以替代它，并摆脱它的陷阱。

Let's illustrate those downsides first with an example. Here we have a Date  value object with a timestamp variable, format function and static constructor called now.

让我们先用一个例子来说明这些缺点。这里我们有一个 Date 值对象，它有一个时间戳变量、format 函数和一个名为 now 的静态构造函数。

```php
class Date

{

    public int $timestamp;

    public static function now(): self { /* … */ }

    public function format(): string { /* … */ }


    // …

}

Next, we have an invoice with a payment date:

接着，我们有一个带有付款日期的发票：

```php
class Invoice

{

    public ?Date $paymentDate = null; 

    // …

}

```

The payment date is nullable because invoices can be pending and not yet have a payment date.

付款日期是可空的，因为发票可能处于待处理状态，还没有付款日期。

As a side note: take a look at the nullable notation; I've already mentioned it but haven't shown it until now. We've prefixed Date  with a question mark, indicating that it can either be Date  or null . We've also added a default = null  value, ensuring the value is never uninitialized to prevent all those runtime errors you might encounter.

作为旁注：看看可空类型的表示法；我之前已经提到过，但直到现在才展示。我们在 Date 前面加了一个问号，表示它可以是 Date 或 null。我们还添加了默认值 = null，确保值永远不会未初始化，以防止你可能遇到的所有运行时错误。

Back to our example: what if we want to do something with our payment date's timestamp?

回到我们的例子：如果我们想对付款日期的时间戳做些什么呢？

```php
$invoice->paymentDate->timestamp;

```

Since we're not sure `$invoice->paymentDate`  is a Date  or null , we risk running into runtime errors:
```
// Trying to get property 'timestamp' of non-object 
```
由于我们不确定 $invoice->paymentDate 是 Date 还是 null，我们可能会遇到运行时错误：
```
// 尝试获取非对象的属性 'timestamp' 
```
Before PHP 7.0, you'd use isset  to prevent those kinds of errors:

在 PHP 7.0 之前，你会使用 isset 来防止这些错误：
```php
isset($invoice=>paymentDate) 

    ? $invoice=>paymentDate=>timestamp 
    : null;

```

That's rather verbose, though, and is why a new operator was introduced: the null coalescing operator.

这相当冗长，这就是为什么引入了一个新操作符：空合并操作符。

```php
$invoice->paymentDate->timestamp ?? null;

```

This operator will automatically perform an isset  check on its left-hand operand. If that returns false, it will return the fallback provided by its righthand operand. In this case, the payment date's timestamp or null. It is a nice addition that reduces the complexity of our code.

这个操作符会自动对其左操作数执行 isset 检查。如果返回 false，它将返回右操作数提供的后备值。在这种情况下，是付款日期的时间戳或 null。这是一个很好的补充，减少了我们代码的复杂性。

PHP 7.4 added another null coalescing shorthand: the null coalescing assignment operator. This one not only supports the default value fallback, but will also write it directly to the left-hand operand. It looks like this:

PHP 7.4 添加了另一个空合并简写：空合并赋值操作符。这个操作符不仅支持默认值后备，还会直接将其写入左操作数。它看起来像这样：

```php
$temporaryPaymentDate = $invoice->paymentDate ??= Date=:now();

```

So if the payment date is already set, we'll use that one in $temporaryPaymentDate, otherwise we'll use Date=:now()  as the fallback for $temporaryPaymentDate  and also write it to $invoice=>paymentDate  immediately.A more common use case for the null coalescing assignment operator is a memoization function: a function that stores the result once it's calculated:

所以如果付款日期已经设置，我们将在 $temporaryPaymentDate 中使用它，否则我们将使用 Date=:now() 作为 $temporaryPaymentDate 的后备值，并立即将其写入 $invoice=>paymentDate。空合并赋值操作符的一个更常见的用例是记忆化函数：一个在计算结果后存储结果的函数：

```php
function match_pattern(string $input, string $pattern) {

    static $cache = [];

    return $cache[$input][$pattern] ??= 

        (function (string $input, string $pattern) {

            preg_match($pattern, $input, $matches);

            return $matches[0];

        })($input, $pattern);

}

```

This function will perform a regex match on a string with a pattern, but if the same string and same pattern are provided, it will simply return the cached result. Before we had the null coalescing operator assignment, we'd need to write it like so:

这个函数将对字符串执行正则表达式匹配，但如果提供了相同的字符串和相同的模式，它将简单地返回缓存的结果。在我们有空合并操作符赋值之前，我们需要这样写：

```php
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

```

There's one more null-oriented feature in PHP added in PHP 8: the nullsafe operator. 

PHP 8 中添加了另一个面向 null 的特性：空安全操作符。

Take a look at this example:

看看这个例子：

```php
$invoice->paymentDate->format();

```

What happens if our payment date is null? You'd again get an error:

如果我们的付款日期是 null 会发生什么？你会再次得到一个错误：
```
// Call to a member function format() on null
```
Your first thought might be to use the null coalescing operator, but that wouldn't work:

// 在 null 上调用成员函数 format() 你首先想到的可能是使用空合并操作符，但那不会起作用：

```php
$invoice=>paymentDate=>format('Y-m-d') =? null;

```

The null coalescing operator doesn't work with method calls on null . So before PHP 8, you'd need to do this:

空合并操作符不能用于在 null 上调用方法。所以在 PHP 8 之前，你需要这样做：

```php
$paymentDate = $invoice=>paymentDate;
$paymentDate ? $paymentDate=>format('Y-m-d') : null;

```

Fortunately there's the nullsafe operator which will only perform method calls when possible and otherwise return null  instead:

幸运的是，有空安全操作符，它只会在可能时执行方法调用，否则返回 null：

```php
$invoice=>getPaymentDate()?=>format('Y-m-d');

```

Dealing with null — there's another way I started this section saying null is called a "billion-dollar mistake", but next, I showed you three ways PHP is embracing null with fancy syntax. The reality is that null is a frequent occurrence in PHP, and it's a good thing we have syntax to deal with it in a sane way. However, it's also good to look at alternatives to using null altogether. One such alternative is the null object pattern.

Dealing with null — there's another way 我在本节开始时说 null 被称为"十亿美元的错误"，但接下来，我向你展示了 PHP 用花哨的语法拥抱 null 的三种方式。现实是 null 在 PHP 中经常出现，我们有语法以合理的方式处理它是件好事。然而，看看完全替代 null 的替代方案也是好的。其中一个替代方案是空对象模式。

Instead of one Invoice  class that manages internal state about whether it's paid or not; let's have two classes: PendingInvoice  and PaidInvoice . The PendingInvoice implementation looks like this:

不是用一个 Invoice 类来管理关于是否已付款的内部状态；让我们有两个类：PendingInvoice 和 PaidInvoice。PendingInvoice 的实现如下：

```php
class PendingInvoice implements Invoice

{

    public function getPaymentDate(): UnknownDate 

    {

        return new UnknownDate();

    }

}

```

PaidInvoice  looks like this:

PaidInvoice 看起来像这样：

```php
class PaidInvoice implements Invoice

{

```

    // …

```php
    public function getPaymentDate(): Date 

    {

        return $this=>date;

    }

}

```

Next, there's an Invoice  interface:

接下来，有一个 Invoice 接口：

```php
interface Invoice

{

    public function getPaymentDate(): Date;

```

}Finally, here are the two date classes:

}最后，这里是两个日期类：

```php
class Date 

{

```

    // …

```php
}

class UnknownDate extends Date

{

    public function format(): string

    {

        return '/';

    }

}

```

The null object pattern aims to replace null  with actual objects, objects that behave differently because they represent the "absence" of the real object. Another benefit of using this pattern is that classes become more representative of the real world: 

instead of a "date or null", it's a "date or unknown date", instead of an "invoice with a state" it's a "paid invoice or pending invoice". You wouldn't need to worry about null anymore.

空对象模式旨在用实际对象替换 null，这些对象的行为不同，因为它们代表真实对象的"缺失"。使用这种模式的另一个好处是类变得更代表现实世界：不是"日期或 null"，而是"日期或未知日期"，不是"带状态的发票"，而是"已付款发票或待处理发票"。你不再需要担心 null。

```php
$invoice=>getPaymentDate()=>format(); // A date or '/'

```

You might not like this pattern, but it's important to know that the problem can be solved this way.

你可能不喜欢这种模式，但重要的是要知道问题可以这样解决。

Changing types Something happened in the above code samples that I wrote down as a fact, yet it's a significant addition to PHP's type system. We were able to change method signatures during inheritance. Take a look at the Invoice  interface:

Changing types 在上面的代码示例中发生了一些事情，我把它写成了一个事实，但这是 PHP 类型系统的一个重要补充。我们能够在继承期间更改方法签名。看看 Invoice 接口：

```php
interface Invoice

{

    public function getPaymentDate(): Date;

}

```

It declares the return type of getPaymentDate  as Date , yet we changed it in our PendingInvoice  to UnknownDate :

它将 getPaymentDate 的返回类型声明为 Date，但我们在 PendingInvoice 中将其更改为 UnknownDate：

```php
class PendingInvoice implements Invoice

{

    public function getPaymentDate(): UnknownDate 

    {

```

        /* … */

```php
    }

}

```

This powerful technique is called type variance; it's supported as of PHP 7.4. It's so powerful (and a little complex) that we'll spend a whole chapter on the topic later in this book. For now, all you need to know is that return types and input parameter types are allowed to change during inheritance, but both have different rules to follow.

这种强大的技术称为类型变体；从 PHP 7.4 开始支持。它如此强大（而且有点复杂），以至于我们将在本书后面用一整章来讨论这个话题。现在，你只需要知道返回类型和输入参数类型在继承期间允许更改，但两者都有不同的规则要遵循。

Another interesting detail has to do with nullable types. There's a difference between a nullable type using ? and a default = null  value; you've seen them used together already in a previous example. The difference is this: if you make a type nullable inPHP, you're still expected to pass something to that function; you can't just skip the parameter:

另一个有趣的细节与可空类型有关。使用 ? 的可空类型和默认值 = null 之间有区别；你已经在之前的例子中看到它们一起使用了。区别在于：如果你在 PHP 中使类型可空，你仍然需要向该函数传递一些东西；你不能只是跳过参数：

```php
function createOrUpdate(?Offer $offer): void

{

```

    // …

```php
}

createOrUpdate();

```

// Uncaught ArgumentCountError: 

//     Too few arguments to function createOrUpdate(),

//     0 passed and exactly 1 expected So by adding an explicit = null  default value, you're allowed to omit the value altogether:

//     传递了 0 个参数，期望正好 1 个 所以通过添加显式的 = null 默认值，你可以完全省略该值：

```php
function createOrUpdate(?Offer $offer = null): void

{

```

    // …

```php
}

createOrUpdate();

```

Unfortunately, because of backwards compatibility, there's a little quirk with this system. If you assign a default = null  value to a variable, it'll always be nullable. Regardless of whether the type is explicitly made nullable or not, so this will be allowed:

不幸的是，由于向后兼容性，这个系统有一个小怪癖。如果你给变量分配一个默认值 = null，它将始终是可空的。无论类型是否显式设为可空，所以这是允许的：

```php
function createOrUpdate(Offer $offer = null): void

{

```

    // …

```php
}

createOrUpdate(null); 

```

Union and Other Types There are still a few more things worth mentioning in this chapter, and the most excit -

ing one is union types. They allow you to type hint a variable with several types. Note: 

the input needs to be one of those declared types. Here's an example:

Union and Other Types 本章中还有几件值得提及的事情，最令人兴奋的是联合类型。它们允许你用多种类型对变量进行类型提示。注意：输入需要是那些声明的类型之一。这是一个例子：

```php
interface Repository 

{

    public function find(int|string $id);

}

```

Be careful not to overuse union types, though. Too many types in the same union can indicate that this function is trying to do too much at once.

不过，要注意不要过度使用联合类型。同一个联合中有太多类型可能表明这个函数试图一次做太多事情。

For example: a framework might allow you to return both a Response  and View  object from controller methods. Sometimes it's convenient to directly return a View , while other times you want to have fine-grained control over the response. These are cases where a union type on Response|View  is fine. On the other hand, if you have a functionthat accepts a union of array|Collection|string , it's probably an indication that the function has to do too many things. It's best to think about finding a common ground in those cases; maybe only accept Collection  or array .

例如：框架可能允许你从控制器方法返回 Response 和 View 对象。有时直接返回 View 很方便，而其他时候你想要对响应进行细粒度控制。这些情况下 Response|View 的联合类型是可以的。另一方面，如果你有一个接受 array|Collection|string 联合类型的函数，这可能表明该函数必须做太多事情。最好考虑在这些情况下找到共同点；也许只接受 Collection 或 array。

Finally, there are three more built-in types available.

最后，还有三个更多的内置类型可用。

There's the static  return type available in PHP 8. It indicates that a function returns the class where that function was called from. It differs from self  since that one always refers to the parent class, while static  can also indicate the child class:

PHP 8 中提供了 static 返回类型。它表示函数返回调用该函数的类。它与 self 不同，因为 self 总是指父类，而 static 也可以表示子类：

abstract class Parent

```php
{

    public static function make(): static { /* … */ }

}

class Child extends Parent { /* … */ }
$child = Child=:make();

```

In this example, static analysis tools and IDEs now know that $child  is an instance of Child . If self  was used as a return type, they would think it was an instance of Parent . Also note that the static  keyword and static  return type are two different concepts; they just happen to have the same name (which is the case in many other languages).

在这个例子中，静态分析工具和 IDE 现在知道 $child 是 Child 的实例。如果 self 用作返回类型，它们会认为它是 Parent 的实例。还要注意 static 关键字和 static 返回类型是两个不同的概念；它们只是碰巧有相同的名称（这在许多其他语言中也是如此）。

There's also the void  return type added in PHP 7.1. It checks whether nothing is returned from a function. Note that void  cannot be combined into a union.

还有 PHP 7.1 中添加的 void 返回类型。它检查函数是否没有返回任何内容。注意 void 不能组合到联合类型中。

Finally, there's the mixed  type, also available as of PHP 8. mixed can be used to type hint "anything". It's a shorthand for the union of array|bool|callable|int|float|null|object|resource|string . Think of mixed  as the opposite of void .

最后，还有 mixed 类型，也从 PHP 8 开始可用。mixed 可用于类型提示"任何东西"。它是 array|bool|callable|int|float|null|object|resource|string 联合类型的简写。将 mixed 视为 void 的反面。

Generics and Enums There are still two major features missing in PHP's type system today: generics and enums. I wish I could write about them in this book, but unfortunately, they aren't supported by the language yet.

Generics and Enums 今天 PHP 的类型系统中仍然缺少两个主要特性：泛型和枚举。我希望能在本书中写它们，但不幸的是，语言还不支持它们。

There have been efforts in the past to add both features, but there hasn't been any consensus about how enums should be implemented, and generics would have too large an impact on runtime performance.

过去曾努力添加这两个特性，但关于如何实现枚举还没有达成共识，而泛型对运行时性能的影响太大。

This raises an interesting question: why do we need to check types at runtime? Isn't that too late? If something goes wrong, the program crashes anyway. That's exactly the topic we'll look at in-depth in the next chapter.

这提出了一个有趣的问题：为什么我们需要在运行时检查类型？那不是太晚了吗？如果出现问题，程序无论如何都会崩溃。这正是我们将在下一章深入探讨的话题。
