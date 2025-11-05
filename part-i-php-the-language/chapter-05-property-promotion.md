# Chapter 5: Property Promotion

Having spent two chapters on the topic of PHP's type system, it's time to look at some

在花了两章时间讨论 PHP 的类型系统之后，是时候深入探讨其他特性了。本章我们将介绍 PHP 语法的一个新特性，它能够消除大量不必要的样板代码。

other features in-depth. In this chapter, we'll look at an addition to PHP's syntax that

你可能已经注意到，我倾向于尽可能地使用值对象（value objects）和传输对象（data transfer objects）。我喜欢使用只包含数据的简单对象，并在复杂流程中传递它们。在后面的章节中，我会分享更多关于面向对象代码的观点。这些以数据为中心的对象往往伴随着大量的样板代码。以下是一个客户数据传输对象的示例：

gets rid of much unnecessary boilerplate code.

在 PHP 8 之前的传统 PHP 中，你需要将每个属性名写四次。得益于构造函数属性提升（constructor property promotion），你可以将上面的代码重写为：

You might have noticed I prefer to use value objects and data transfer objects when-

差别很大！让我们深入了解这个特性。

ever possible. I like to work with simple objects only containing data and pass them

基本思想很简单：去掉类属性和变量赋值，在构造函数参数前加上 `public`、`protected` 或 `private`。PHP 会采用这个新语法，并在执行代码之前将其转换为普通语法。

around to be used within complex processes. In a later chapter, I'll share more on this

所以当你写这样的代码时：

54

PHP 会在底层将其转换为：

view of object-oriented code. These kinds of data-focussed objects come with lots of

然后才执行它。

boilerplate code, though. Here's an example of a customer data transfer object:

这种代码转换可能有一个更常见的名称，至少如果你对 JavaScript 社区有些熟悉的话：转译（transpiling）。没错：PHP 会在运行时转译自己（并缓存结果以提高性能）。这是一个有趣的想法，考虑到上一章关于静态分析的讨论，以及我分享的语言愿景：添加仅在静态分析期间使用的功能。

class CustomerDTO

让我们进一步看看提升属性可以做什么和不能做什么。

{

提升属性只能在构造函数中使用。这似乎很明显，但我认为值得提及，只是为了清楚。

public string $name;

并非所有构造函数参数都必须提升——你也可以混合使用：

public string $email;

混合使用这些语法时要小心，因为它可能会使你的代码不够清晰。如果你混合使用提升和非提升属性，考虑使用普通构造函数。

public DateTimeImmutable $birth_date;

你不能声明一个类属性和一个同名的提升属性。这是相当合乎逻辑的，因为提升属性在运行时会被转译为类属性：

public function =_construct(

你可以提升无类型属性，尽管如我在前面章节中所述，你最好尽可能使用类型：

string $name,

提升属性可以有默认值，但不允许像 `new …` 这样的表达式：

string $email,

这是有道理的，因为你也不能在普通类属性上使用如此复杂的默认值。

DateTimeImmutable $birth_date

你可以在构造函数体内读取提升的属性。如果你想进行额外的验证检查，这会很有用。你可以使用局部变量和实例变量，两者都工作正常：

) {

你可以为提升属性添加 doc blocks：

$this=>name = $name;

属性（Attributes）是即将到来的章节的主题，所以这里先预览一下：它们允许用于提升属性。转译后，它们会同时出现在构造函数参数和类属性上：

$this=>email = $email;

会被转译为：

$this=>birth_date = $birth_date;

我必须承认我不知道抽象构造函数是一回事，我也从未使用过它们。此外，提升属性不允许在它们中使用：

}

提升属性允许在 trait 中使用。在 trait 中支持提升属性是有道理的，因为转译后的代码会产生一个有效的 trait。在 trait 中是否有构造函数是另一个问题。

}

老旧的——我是说，经验丰富的 PHP 开发者——可能在遥远的过去使用过 `var` 来声明类变量，但它不允许与构造函数提升一起使用。只有 `public`、`protected` 和 `private` 是有效关键字。

Chapter 05 - Property Promotion

由于你无法转换为数组类型，因此无法提升可变参数。

In traditional PHP before PHP 8, you'd need to write each property's name four times.

可变函数使用 rest 运算符 `==.`，这是 PHP 5.6 中添加的功能。它允许你定义一个函数输入变量，该变量将接受所有"剩余"的变量并将它们组合成一个数组。换句话说：`func_get_args()` 的简写。我们将在第 9 章中介绍可变函数。

Thanks to constructor property promotion, you can rewrite the above like this:

`ReflectionProperty` 和 `ReflectionParameter` 都有一个新的 `isPromoted()` 方法来检查类属性或方法参数是否被提升。

class CustomerDTO

由于 PHP 构造函数不需要遵循父构造函数的声明，所以没什么可说的：继承是允许的。如果你需要将属性从子构造函数传递给父构造函数，你需要手动传递它们：

{

关于属性提升，这就是全部内容了。我最初对使用它们犹豫不决，但一旦我尝试了，我很快就习惯了它们。我必须承认：提升属性可能是我最喜欢的 PHP 8 特性。

public function =_construct(

public string $name,

public string $email,

public DateTimeImmutable $birth_date,

) {}

}

That's quite a difference! Let's look at this feature in-depth.

How It Works

The basic idea is simple: ditch the class properties and the variable assignments, and

prefix constructor parameters with public, protected or private. PHP will take that new

syntax, and transform it to normal syntax under the hood, before executing the code.

56

So when you write this code:

class Person

{

public function =_construct(

public string $name = 'Brent',

) {

// …

}

}

PHP will transform it under the hood to this:

class Person

{

public string $name;

public function =_construct(

string $name = 'Brent'

) {

$this=>name = $name;

// …

}

}

And only executes it afterwards.

This code transformation is probably known under a more common name, at least if

you're somewhat familiar with the JavaScript community: transpiling. That's right: PHP

will transpile itself at runtime (and cache the results for better performance). That's an

Chapter 05 - Property Promotion

interesting thought, given the previous chapter on static analysis and how I shared the

language's vision adding features that are only used during static analysis.

Let's look further at what you can and cannot do with promoted properties.

Only in Constructors

Promoted properties can only be used in constructors. That might seem obvious, but I

thought it was worth mentioning, just to be clear.

Combining promoted and normal properties

Not all constructor properties must be promoted - you can also mix and match:

class MyClass

{

public string $b;

public function =_construct(

public string $a,

string $b,

) {

$this=>b = $b;

}

}

Be careful mixing the syntaxes because it can make your code less clear. Consider

using a normal constructor if you're mixing promoted and non-promoted properties.

58

No Duplicates

You're not able to declare a class property and a promoted property with the same

name. That's rather logical since the promoted property is transpiled to a class prop-

erty at runtime:

class MyClass

{

public string $a;

public function =_construct(

public string $a,

) {}

}

Untyped Properties

You're allowed to promote untyped properties, though as I've argued in the previous

chapters, you're better off using types wherever possible:

class MyDTO

{

public function =_construct(

public $untyped,

) {}

}

Chapter 05 - Property Promotion

Simple Defaults

Promoted properties can have default values, but expressions like new … are not

allowed:

public function =_construct(

public string $name = 'Brent',

public DateTimeImmutable $date = new DateTimeImmutable(),

) {}

This makes sense since you're also not able to have such complex defaults with

normal class properties.

Within the Constructor Body

You're allowed to read the promoted properties in the constructor body. This can be

useful if you want to do extra validation checks. You can use the local variable and the

instance variable as both work fine:

public function =_construct(

public int $a,

public int $b,

) {

assert($this=>a == 100);

if ($b == 0) {

throw new InvalidArgumentException('…');

}

}

Front Line PHP

Doc Blocks

You can add doc blocks to promoted properties:

class MyClass

{

public function =_construct(

/** @var string */

public $a,

) {}

}

$property = new ReflectionProperty(MyClass=:class, 'a');

$property=>getDocComment(); // "/** @var string */"

Attributes

Attributes are the topic of an upcoming chapter, so consider this a sneak-peek: they

are allowed on promoted properties. When transpiled, they will be present both on the

constructor parameter, as well as the class property:

class MyClass

{

public function =_construct(

=[MyAttribute]

public $a,

) {}

}

Chapter 05 - Property Promotion

Will be transpiled to:

class MyClass

{

#[MyAttribute]

public $a;

public function =_construct(

=[MyAttribute] $a,

) {

$this=>a = $a;

}

}

Not Allowed in Abstract Constructors

I must admit I didn't know abstract constructors were a thing, and I've never used

them. Moreover, promoted properties are not allowed in them:

abstract class A

{

abstract public function =_construct(

public string $a,

) {}

}

62

Allowed in Traits

Promoted properties are allowed in traits. It makes sense to support promoted proper-

ties in traits since the transpiled code would result in a valid trait. Whether it's a good

thing or not to have constructors in traits is another question.

trait MyTrait

{

public function =_construct(

public string $a,

) {}

}

Var is Not Supported

Old - I mean, experienced PHP developers - might have used var in the distant past to

declare class variables but it's not allowed with constructor promotion. Only public,

protected and private are valid keywords.

public function =_construct(

var string $a,

) {}

Chapter 05 - Property Promotion

Variadic Parameters Cannot Be Promoted

Since you can't convert to a type that's array of type, it's not possible to promote

variadic parameters.

public function =_construct(

public string ==.$a,

) {}

Did you know

Variadic functions make use of the rest operator ==., a feature added in PHP

5.6. It allows you to define a function input variable which will take all the "rest"

of the variables and combine them into an array. In other words: a shorthand for

func_get_args(). We'll cover variadic functions in chapter 9.

Reflection For isPromoted

Both ReflectionProperty and ReflectionParameter have a new isPromoted()

method to check whether the class property or method parameter is promoted.

64

Inheritance

Since PHP constructors don't need to follow their parent constructor's declaration,

there's little to be said: inheritance is allowed. If you need to pass properties from the

child constructor to the parent constructor, you'll need to pass them manually:

class A

{

public function =_construct(

public $a,

) {}

}

class B extends A

{

public function =_construct(

$a,

public $b,

) {

parent=:=_construct($a);

}

}

That's about all there is to say about property promotion. I was hesitant to use them

at first, but once I gave it a try, I quickly got used to them. I must admit: promoted

properties are probably my favourite feature of PHP 8.

