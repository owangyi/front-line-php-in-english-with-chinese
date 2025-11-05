# Chapter 7: Attributes

I've mentioned them twice before, and we've finally arrived at the topic: attributes. I

属性（Attributes）是 PHP 8 引入的元数据功能，允许为类、方法、属性等添加注解信息。本章详细介绍了属性的使用方式、创建自定义属性、通过反射读取属性等内容。

remember doing my thesis back in college, and one of the central topics was "annota-

让我们看一个在真实场景中使用属性的例子：

tions in PHP". At that time there were custom annotations parsers, essentially parsing

这里我们看到属性用于事件监听器：当方法被 `ListensTo` 标记时，注册事件监听器时可以使用这个属性来构建哪个方法处理哪个事件的映射。

doc block strings on the fly and interpreting those as annotations. There was a big

当我在网上展示 ListensTo 示例时，有人告诉我你可以直接查看方法的类型参数来知道它处理什么事件，添加专用属性似乎是冗余的。对于简单的应用程序，我同意，但让我们考虑以下示例。

debate about whether annotations should or shouldn't be added to the core. It's great

想象一个 `LoggableEvent` 接口，事件可以实现它：

to see them finally arrive in PHP, albeit with a different name: attributes.

以及一个 `MailLogEventSubscriber`：

Attributes can be used to add meta data to your code: stuff that would otherwise

现在想象——因为业务需要——一些 `LoggableEvent` 对象应该通过发送日志邮件来处理，但不是全部。如果你依赖方法签名来确定它们应该处理什么事件，你最终会得到这样的代码：

end up in config files or other places. One of the best-known examples is routing in

使用属性，你可以这样写：

Symfony, where you could write this:

现在，如果你正在构建一个只有几十个事件的应用程序，简单的方法就可以了。但如果你要处理数千个事件，就会变得很繁琐。在这些情况下，我更喜欢显式的方法，因为它最终会节省时间。

class BlogController

回到我们的例子。这个 `ListensTo` 属性是如何工作的？首先，自定义属性是简单的类，用 `=[Attribute]` 属性注解。看起来是这样的：

{

就是这样——非常简单，对吧？记住属性的目标：它们旨在为类和方法添加元数据，仅此而已。

/**

我们仍然需要读取该元数据并在某处注册我们的订阅者。你可以在实例化事件总线时读取属性，在我的 Laravel 项目中，我会使用服务提供者来这样做。

* @Route("/blog", name="blog_index")

在 Laravel 中，服务提供者用于在启动时设置应用程序。可以有多个服务提供者，每个都做自己的事情。常见的用例是容器注册，这是我们在下一章中要讨论的主题。

*/

在这个例子中，我们会从某些文件中读取属性并将它们注册为事件订阅者。

public function index()

以下是样板设置，提供一些上下文：

{

你可以看到我们在 for 循环中使用了 `as [$event, $listener]` 语法。这被称为数组解构，也是我们将在下一章中讨论的内容。

// ...

最有趣的是 `resolveListeners` 的实现。它是这样的：

}

使用反射，我们可以从类的方法中读取属性，并使用 `$attribute=>newInstance()` 调用实例化自定义属性类。这是一个重要的细节：我们的属性对象只有在调用 `newInstance()` 时才会被构造，而不是在加载时；它不会事先神奇地发生。当构造属性时，它会接受我们在编写 `=[ListensTo(OrderCreatedEvent=:class)]` 时给它的参数，并将它们传递给 `ListensTo` 构造函数。

}

这意味着，从技术上讲，你甚至不需要构造自定义属性。你可以直接调用 `$attribute=>getArguments()`。另一方面，实例化类意味着你可以使用构造函数的灵活性以任何你喜欢的方式解析输入。

78

另一个值得提及的是 `ReflectionMethod=:getAttributes()` 的使用——返回方法的所有属性的函数。你可以传递两个参数给它，以过滤其输出。为了理解这种过滤，首先你需要了解关于属性的另一件事：可以在同一个方法、类、属性或常量上添加多个属性。例如，你可以这样做：

With attributes in PHP 8, it would look like this:

我提出 `Autowire` 属性只是一个例子。它表示这个类可以被依赖容器自动装配——这是我们在后面的章节中要深入讨论的主题。

class BlogController

假设你正在解析控制器路由，只对 `Route` 属性感兴趣。在这种情况下，你可以将 `Route` 类作为过滤器传递：

{

你可以传递给 `getAttributes()` 的第二个参数会改变过滤的方式。默认情况下，它只会匹配完全匹配给定类名的属性。但是，通过使用 `ReflectionAttribute=:IS_INSTANCEOF`，你可以检索实现给定接口的所有属性。例如，假设你正在解析由几个潜在属性组成的容器定义：

=[Route('/blog', name: 'blog_index')]

如果我们的 `Autowire` 属性实现了 `ContainerAttribute` 接口，只有那个会被返回，而不是 `Route` 属性。这是一个很好的简写，内置在核心中。

public function index()

现在你已经了解了属性在实践中是如何工作的，是时候了解更多理论了，确保你彻底理解它们。首先，我之前简要提到过：属性可以添加到多个位置。你可以将它们添加到类中，以及匿名类中：

{

属性和常量：

// ...

方法和函数：

}

以及闭包：

}

还有方法和函数参数：

What about the syntax?

如果你想更精细地控制自定义属性的使用位置，可以配置它们，使其只能在特定位置使用。例如，你可以让 `ClassAttribute` 只能用于类，而不能用于其他地方。

It took months before a final syntax for attributes was decided. Options went

通过向属性类上的 `Attribute` 属性传递标志来选择此行为。

from =< and => to @@ and other exotic variations. The simplest option — @ —

它看起来是这样的：

wasn't possible to use because that's already the error suppression operator.

以下标志可用：

Finally, we settled on =[], the same syntax used by Rust annotations. Its benefit

这些是位掩码标志，因此你可以使用二进制 OR 操作组合它们。

is that it can group several attributes at once.

继续，属性可以在 doc blocks 之前或之后声明：

The advantage of attributes is that you don't have to parse a blob of text at runtime

属性可以接受零个、一个或多个参数，这些参数由属性的构造函数定义：

anymore; PHP has built-in reflection support for them. We'll cover all of it in depth in

关于你可以传递给属性的参数类型，你已经看到允许常量、使用 `=:class` 的类名和标量类型。实际上，属性只接受所谓的常量表达式作为输入参数。这意味着允许标量表达式——甚至位移——以及常量、数组和数组解包、布尔表达式和空合并运算符：

this chapter!

但是，你不能给属性一个类的新实例或静态方法调用——这些不是常量表达式：

Chapter 07 - Attributes

默认情况下，属性不能在同一位置重复两次：

Rundown

但是可以改变这种行为，再次使用配置标志，就像目标配置一样：

Let's look at another example of attributes in the wild:

请注意，所有配置标志只有在调用 `$attribute=>newInstance()` 时才会被验证，而不是更早。这意味着在错误的位置使用属性可能会被忽略，除非你通过反射或静态分析评估该属性。

use Support\Attributes\ListensTo;

一旦属性的基础 RFC 被接受，就有了向核心添加内置属性的新机会。一个这样的例子是 `=[Deprecated]` 属性，以及 `=[Jit]` 属性。我相信我们将来会看到越来越多的内置属性，但现在，一个都不存在。

class ProductSubscriber

不过，PhpStorm IDE 做了一件非常有趣的事情：他们在 PhpStorm 中添加了自己的自定义属性。这些属性不是你的代码库中的真实类，但正如我们所看到的，只有在调用 `$reflectionAttribute=>newInstance()` 时才需要真实的属性类。PhpStorm 提供的内置属性无法实例化，因为它们不是真实的类；但它们可以被 IDE 理解以添加更丰富的静态分析选项。一个例子是 `=[ArrayShape]` 属性，它可以告诉 PhpStorm 数组中到底有什么：

{

通过添加这样的属性，PhpStorm 现在确切知道 `legacyFunction` 返回的数组中的键是什么，以及每个键的类型。不过，我会犹豫是否编写依赖于数组键和类型的代码（我会为此使用 DTO）。但是，`=[ArrayShape]` 是记录遗留代码库的绝佳方法，在那里你并不总是能控制其设计。顺便说一下，PhpStorm 还提供了更多内置属性：`=[Deprecated]`、`=[Immutable]`、`=[Pure]`、`=[ExpectedValues]`，甚至更多。

=[ListensTo(ProductCreated=:class)]

看到 PhpStorm 如何拥抱我们之前讨论的静态分析思维很有趣：我们不需要进行任何运行时检查，因为静态分析器（在这种情况下是 PhpStorm）可以在运行代码之前告诉我们做错了什么，这要归功于属性。不过，我们需要小心，静态分析工具要保持它们之间的一些互操作性。如果每个工具都决定实现自己的属性版本，它不会使开发人员体验更好。

public function onProductCreated(ProductCreated $event) { /* … */ }

看看在核心和第三方静态分析器中添加什么样的属性，以及它们如何协同工作，这将很有趣。

=[ListensTo(ProductDeleted=:class)]

public function onProductDeleted(ProductDeleted $event) { /* … */ }

}

Here we see attributes being used for event listeners: whenever a method is marked

with ListensTo. When registering event listeners, we could use this attribute to build a

mapping of which methods handle which events.

Redundant attributes?

When I showed the ListensTo example online, some people told me you could

just look at the method's typed parameter to know what event it handles, and

adding a dedicated attribute seemed redundant. For simple applications, I'd

agree, but let's consider the following example.

Imagine a LoggableEvent interface that events may implement:

80

interface LoggableEvent

{

public function getEventName();

}

And a MailLogEventSubscriber:

class MailLogEventSubscriber

{

public function handleLoggableEvent(LoggableEvent $event)

{

// …

}

}

Now imagine — because the business requires it — that some LoggableEvent

objects should be handled by sending a log mail, but not all. If you're relying on

the method signatures to determine what events they should handle, you will

end up with something like this:

class MailLogEventSubscriber

{

public function handleOrderCreatedEvent(

OrderCreatedEvent $event

): void {

$this->actuallyHandleTheEvent($event);

}

public function handleInvoiceCreatedEvent(

InvoiceCreatedEvent $event

): void {

$this->actuallyHandleTheEvent($event);

}

Chapter 07 - Attributes

public function handleInvoicePaidEvent(

InvoicePaidEvent $event

): void {

$this->actuallyHandleTheEvent($event);

}

private function actuallyHandleTheEvent(

LoggableEvent $event

): void {

// …

}

}

Using attributes, however, would allow you to write something like this:

class MailLogEventSubscriber

{

#[

ListensTo(OrderCreatedEvent::class),

ListensTo(InvoiceCreatedEvent::class),

ListensTo(InvoicePaidEvent::class),

]

public function handleLoggableEvent(LoggableEvent $event)

{

// …

}

}

Now, if you're building an application with only a few dozen events, the simple

approach is fine. If you're dealing with thousands of events, though, it becomes

cumbersome. It's those cases where I prefer the explicit approach because it

saves time in the end.

82

Back to our example. How would this ListensTo attribute work under the hood? First

of all, custom attributes are simple classes, annotated with the =[Attribute] attri-

bute. Here's what it would look like:

=[Attribute]

class ListensTo

{

public function =_construct(

public string $event

) {}

}

That's it — pretty simple, right? Keep in mind the goal of attributes: they are meant to

add meta data to classes and methods, nothing more.

We still need to read that meta data and register our subscribers somewhere. You

would read attributes when you're instantiating the event bus, and in my Laravel proj-

ects, I would use a service provider to do so.

In Laravel, service providers are used to set up the application when booting.

There can be multiple service providers, each doing their own thing. A common

use case is container registration, a topic we'll cover in an upcoming chapter.

In this example, we'd read the attributes from certain files and register them as

event subscribers.

Chapter 07 - Attributes

Here's the boilerplate setup, to provide a little context:

class EventServiceProvider extends ServiceProvider

{

// In real life scenarios,

//  we'd automatically resolve and cache all subscribers

//  instead of using a manual array.

private array $subscribers = [

ProductSubscriber=:class,

];

public function register(): void

{

// The event dispatcher is resolved from the container

$eventDispatcher = $this=>app=>make(EventDispatcher=:class);

foreach ($this=>subscribers as $subscriber) {

// We'll resolve all listeners

//  (methods with the ListensTo attribute)

//  and add them to the dispatcher.

foreach (

$this=>resolveListeners($subscriber)

as [$event, $listener]

) {

$eventDispatcher=>listen($event, $listener);

}

}

}

84

private function resolveListeners(string $subscriberClass): array

{

// Return an array with [eventName => handler] items.

}

}

You can see we're using the as [$event, $listener] syntax in the for-loop.

This is called array destructuring and something we'll also cover in an upcoming

chapter.

Chapter 07 - Attributes

What's most interesting is the implementation of resolveListeners. Here it is:

private function resolveListeners(string $subscriberClass): array

{

$reflectionClass = new ReflectionClass($subscriberClass);

$listeners = [];

foreach ($reflectionClass=>getMethods() as $method) {

$attributes = $method=>getAttributes(ListensTo=:class);

foreach ($attributes as $attribute) {

$listener = $attribute=>newInstance();

$listeners[] = [

// The event that's configured on the attribute

$listener=>event,

// The listener for this event

[$subscriberClass, $method=>getName()],

];

}

}

return $listeners;

}

Using reflection, we can read the attributes from the class' methods, and instantiate

our custom attribute classes with the $attribute=>newInstance() call. This is an im-

portant detail: our attribute objects are only constructed when we call newInstance()

on them and not when they are loaded; it doesn't happen magically beforehand. When

an attribute is constructed it will take the parameters we've given it when writing

86

=[ListensTo(OrderCreatedEvent=:class)], and pass them to the ListensTo construc-

tor.

This means that, technically, you don't even need to construct the custom attribute.

You could call $attribute=>getArguments() directly. On the other hand, instantiating

the class means you've got the constructor's flexibility to parse the input in whatever

way you like.

Another thing worth mentioning is the use of ReflectionMethod=:getAttributes() —

the function that returns all attributes for a method. You can pass two arguments to it,

to filter its output. In order to understand this filtering though, there's one more thing

you need to know about attributes first: it's possible to add several attributes to the

same method, class, property or constant. You could, for example, do this:

=[

Route(Http=:POST, '/products/create'),

Autowire,

]

class ProductsCreateController

{

public function =_invoke() { /* … */ }

}

I came up with the Autowire attribute just as an example. It indicates this class

could be autowired by the dependency container — a topic we'll cover in-depth

in a later chapter.

Chapter 07 - Attributes

Say you're parsing controller routes and you're only interested in the Route attribute.

In that case you can pass the Route class as a filter:

$attributes = $reflectionClass=>getAttributes(Route=:class);

There's a second parameter you can pass to getAttributes() which changes how

the filtering is done. By default it'll only match attributes that exactly match the given

class name. However, by using ReflectionAttribute=:IS_INSTANCEOF, you're able to

retrieve all attributes implementing a given interface. For example, say you're parsing

container definitions that consist of several potential attributes:

$attributes = $reflectionClass=>getAttributes(

ContainerAttribute=:class,

ReflectionAttribute=:IS_INSTANCEOF

);

If our Autowire attribute would implement the ContainerAttribute interface, only that

one would be returned and not the Route attribute. It's a nice shorthand, built into the

core.

Attributes in Depth

Now that you have an idea of how attributes work in practice, it's time for some more

theory, making sure you understand them thoroughly. First of all something I men-

88

tioned briefly before: attributes can be added in several places. You can add them in

classes, as well as anonymous classes:

=[ClassAttribute]

class MyClass { /* … */ }

$object = new =[ObjectAttribute] class () { /* … */ };

Properties and constants:

=[PropertyAttribute]

public int $foo;

=[ConstAttribute]

public const BAR = 1;

Methods and functions:

=[MethodAttribute]

public function doSomething(): void { /* … */ }

=[FunctionAttribute]

function foo() { /* … */ }

As well as closures:

$closure = =[ClosureAttribute] fn () => /* … */;

Chapter 07 - Attributes

And method and function parameters:

function foo(=[ArgumentAttribute] $bar) { /* … */ }

If you want finer control over where your custom attributes are used, it's possible to

configure them so they can only be used in specific places. For example you could

make it so that ClassAttribute can only be used on classes, and nowhere else.

Opting-in this behaviour is done by passing a flag to the Attribute attribute on the

attribute class.

It looks like this:

=[Attribute(Attribute=:TARGET_CLASS)]

class ClassAttribute

{

}

The following flags are available:

Attribute=:TARGET_CLASS

Attribute=:TARGET_FUNCTION

Attribute=:TARGET_METHOD

Attribute=:TARGET_PROPERTY

Attribute=:TARGET_CLASS_CONSTANT

Attribute=:TARGET_PARAMETER

Attribute=:TARGET_ALL

These are bitmask flags, so you can combine them using a binary OR operation.

90

=[Attribute(Attribute=:TARGET_METHOD | Attribute=:TARGET_FUNCTION)]

class FunctionAttribute

{

}

Moving on, attributes can be declared before or after doc blocks:

/** @return void */

=[MethodAttribute]

public function doSomething(): void { /* … */ }

An attribute can take none, one or several arguments, which are defined by the attri-

bute's constructor:

=[Attribute]

class ListensTo

{

public function =_construct(

public string $event

) {}

}

=[ListensTo(ProductCreatedEvent=:class)]

With regards to types of parameters you can pass to an attribute, you've already seen

that constants, class names using =:class and scalar types are allowed. In fact, attri-

butes only accept so called constant expressions as input arguments. This means that

Chapter 07 - Attributes

scalar expressions are allowed — even bit shifts — as well as constants, arrays and

array unpacking, boolean expressions and the null coalescing operator:

=[AttributeWithScalarExpression(1 + 1)]

=[AttributeWithClassNameAndConstants(PDO=:class, PHP_VERSION_ID)]

=[AttributeWithClassConstant(Http=:POST)]

=[AttributeWithBitShift(4 => 1, 4 =< 1)]

However, you can't give attributes a new instance of a class or a static method call for

example - those are not constant expressions:

=[AttributeWithError(new MyClass())]

=[AttributeWithError(MyClass=:staticMethod())]

By default, attributes cannot be repeated twice in the same place:

=[

ClassAttribute,

ClassAttribute,

]

class MyClass { /* … */ }

It is possible to change that behaviour though, again using a configuration flag like

with target configuration:

=[Attribute(Attribute=:IS_REPEATABLE)]

class ClassAttribute

{

}

92

Note that all configuration flags are only validated when calling

$attribute=>newInstance(), not earlier. This means that using an attribute in the

wrong place might go unnoticed unless you're evaluating that attribute via reflection

or static analysis.

Built-In Attributes

Once the base RFC for attributes had been accepted, new opportunities arose to add

built-in attributes to the core. One such example is the =[Deprecated] attribute, as

well as a =[Jit] attribute. I'm sure we'll see more and more built-in attributes in the

future, but right now, none exist.

PhpStorm, the IDE, has done something very interesting though: they have added

their own custom attributes in PhpStorm. These attributes aren't real classes in your

codebase, but as we've seen you only need real attribute classes when you call

$reflectionAttribute=>newInstance(). The built-in attributes shipped by PhpStorm

can't be instantiated, since they aren't real classes; but they can be understood by the

IDE to add richer static analysis options. One example is the =[ArrayShape] attribute,

which can teach PhpStorm what exactly is in an array:

=[ArrayShape([

'key1' => 'int',

'key2' => 'string',

'key3' => 'Foo',

'key3' => Foo=:class,

])]

function legacyFunction(…): array

By adding such an attribute, PhpStorm now knows exactly what keys are in the array

returned by legacyFunction, as well as the type of each key. I would be hesitant

Chapter 07 - Attributes

to write code that relies on array keys and types, though (I'd use DTOs for that).

However, the =[ArrayShape] is an excellent way to document a legacy codebase,

where you don't always have control over its design. There are more built-in attri-

butes shipped by PhpStorm, by the way: =[Deprecated], =[Immutable], =[Pure],

=[ExpectedValues], and even more.

It's interesting to see how PhpStorm embraces the static analysis mindset we've

discussed earlier: we don't need to do any runtime checks since the static analyser

(PhpStorm in this case) can tell us what we're doing wrong before running the code,

thanks to attributes. We need to be careful though, that static analysis tools keep

some interoperability between them. If each tool decides to implement their own

version of attributes, it won't make the developer experience any better.

It'll be interesting to see what kind of attributes get added, both in the core and by

third-party static analysers, and how they manage to work together.

94

