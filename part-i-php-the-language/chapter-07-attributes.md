# CHAPTER 07

## ATTRIBUTES I've mentioned them twice before, and we've finally arrived at the topic: attributes. I remember doing my thesis back in college, and one of the central topics was "annotations in PHP". At that time there were custom annotations parsers, essentially parsing doc block strings on the fly and interpreting those as annotations. There was a big debate about whether annotations should or shouldn't be added to the core. It's great to see them finally arrive in PHP, albeit with a different name: attributes.

Attributes can be used to add meta data to your code: stuff that would otherwise end up in config files or other places. One of the best-known examples is routing in Symfony, where you could write this:

```php
class BlogController

{

```

    /**

     * @Route("/blog", name="blog_index")

     */

```php
    public function index()

    {

```

        // ...

```php
    }

```

}With attributes in PHP 8, it would look like this:

```php
class BlogController

{

```

    =[Route('/blog', name: 'blog_index')]

```php
    public function index()

    {

```

        // ...

```php
    }

}

```

What about the syntax?

It took months before a final syntax for attributes was decided. Options went from =< and => to @@ and other exotic variations. The simplest option — @ — 

wasn't possible to use because that's already the error suppression operator.

Finally, we settled on =[], the same syntax used by Rust annotations. Its benefit is that it can group several attributes at once.

The advantage of attributes is that you don't have to parse a blob of text at runtime anymore; PHP has built-in reflection support for them. We'll cover all of it in depth in this chapter!

Rundown Let's look at another example of attributes in the wild:

```php
use Support\Attributes\ListensTo;

class ProductSubscriber

{

```

    =[ListensTo(ProductCreated=:class)]

```php
    public function onProductCreated(ProductCreated $event) { /* … */ }

```

    =[ListensTo(ProductDeleted=:class)]

```php
    public function onProductDeleted(ProductDeleted $event) { /* … */ }

}

```

Here we see attributes being used for event listeners: whenever a method is marked with ListensTo . When registering event listeners, we could use this attribute to build a mapping of which methods handle which events.

Redundant attributes?

When I showed the ListensTo example online, some people told me you could just look at the method's typed parameter to know what event it handles, and adding a dedicated attribute seemed redundant. For simple applications, I'd agree, but let's consider the following example.

Imagine a LoggableEvent  interface that events may implement:interface LoggableEvent

```php
{

    public function getEventName();

}

```

And a MailLogEventSubscriber :

```php
class MailLogEventSubscriber

{

    public function handleLoggableEvent(LoggableEvent $event)

    {

```

        // …

```php
    }

}

```

Now imagine — because the business requires it — that some  LoggableEvent objects should be handled by sending a log mail, but not all. If you're relying on the method signatures to determine what events they should handle, you will end up with something like this:

```php
class MailLogEventSubscriber

{

    public function handleOrderCreatedEvent(

```

        OrderCreatedEvent $event

```php
    ): void {
$this->actuallyHandleTheEvent($event);

    }

    public function handleInvoiceCreatedEvent(

```

        InvoiceCreatedEvent $event

```php
    ): void {
$this->actuallyHandleTheEvent($event);

    }

    public function handleInvoicePaidEvent(

```

        InvoicePaidEvent $event

```php
    ): void {
$this->actuallyHandleTheEvent($event);

    }

    private function actuallyHandleTheEvent(

```

        LoggableEvent $event

```php
    ): void {

```

        // …

```php
    }

}

```

Using attributes, however, would allow you to write something like this:

```php
class MailLogEventSubscriber

{

```

    #[

        ListensTo(OrderCreatedEvent::class),

        ListensTo(InvoiceCreatedEvent::class),

        ListensTo(InvoicePaidEvent::class),

    ]

```php
    public function handleLoggableEvent(LoggableEvent $event)

    {

```

        // …

```php
    }

}

```

Now, if you're building an application with only a few dozen events, the simple approach is fine. If you're dealing with thousands of events, though, it becomes cumbersome. It's those cases where I prefer the explicit approach because it saves time in the end.Back to our example. How would this ListensTo  attribute work under the hood? First of all, custom attributes are simple classes, annotated with the =[Attribute]  attribute. Here's what it would look like:

=[Attribute]

```php
class ListensTo

{

    public function =_construct(

        public string $event

    ) {}

}

```

That's it — pretty simple, right? Keep in mind the goal of attributes: they are meant to add meta data to classes and methods, nothing more.

We still need to read that meta data and register our subscribers somewhere. You would read attributes when you're instantiating the event bus, and in my Laravel projects, I would use a service provider to do so.

In Laravel, service providers are used to set up the application when booting. 

There can be multiple service providers, each doing their own thing. A common use case is container registration, a topic we'll cover in an upcoming chapter.

In this example, we'd read the attributes from certain files and register them as event subscribers.

Here's the boilerplate setup, to provide a little context:

```php
class EventServiceProvider extends ServiceProvider

{

```

    // In real life scenarios, 

    //  we'd automatically resolve and cache all subscribers

    //  instead of using a manual array.

```php
    private array $subscribers = [

```

        ProductSubscriber=:class,

```php
    ];

    public function register(): void

    {

```

        // The event dispatcher is resolved from the container

```php
$eventDispatcher = $this=>app=>make(EventDispatcher=:class);

        foreach ($this=>subscribers as $subscriber) {

```

            // We'll resolve all listeners

            //  (methods with the ListensTo attribute) 

            //  and add them to the dispatcher.

```php
            foreach (
$this=>resolveListeners($subscriber) 

```

                as [$event, $listener]

```php
            ) {
$eventDispatcher=>listen($event, $listener);

            }       

        }       

```

    }private function resolveListeners(string $subscriberClass): array

```php
    {

```

        // Return an array with [eventName => handler] items. 

```php
    }

}

```

You can see we're using the as [$event, $listener]  syntax in the for-loop. 

This is called array destructuring and something we'll also cover in an upcoming chapter.

What's most interesting is the implementation of resolveListeners . Here it is:

```php
private function resolveListeners(string $subscriberClass): array

{
$reflectionClass = new ReflectionClass($subscriberClass);
$listeners = [];

    foreach ($reflectionClass=>getMethods() as $method) {
$attributes = $method=>getAttributes(ListensTo=:class);

        

        foreach ($attributes as $attribute) {
$listener = $attribute=>newInstance();
$listeners[] = [

```

                // The event that's configured on the attribute

```php
$listener=>event,

    

```

                // The listener for this event 

                [$subscriberClass, $method=>getName()],

```php
            ];

        }

    }

    return $listeners;

}

```

Using reflection, we can read the attributes from the class' methods, and instantiate our custom attribute classes with the $attribute=>newInstance()  call. This is an im -

portant detail: our attribute objects are only constructed when we call newInstance()  

on them and not when they are loaded; it doesn't happen magically beforehand. When an attribute is constructed it will take the parameters we've given it when writing=[ListensTo(OrderCreatedEvent=:class)] , and pass them to the ListensTo  constructor.

This means that, technically, you don't even need to construct the custom attribute. 

You could call $attribute=>getArguments()  directly. On the other hand, instantiating the class means you've got the constructor's flexibility to parse the input in whatever way you like.

Another thing worth mentioning is the use of ReflectionMethod=:getAttributes()  — 

the function that returns all attributes for a method. You can pass two arguments to it, 

to filter its output. In order to understand this filtering though, there's one more thing you need to know about attributes first: it's possible to add several attributes to the same method, class, property or constant. You could, for example, do this:

=[

    Route(Http=:POST, '/products/create'),

    Autowire,

]

```php
class ProductsCreateController

{

    public function =_invoke() { /* … */ }

}

```

I came up with the Autowire  attribute just as an example. It indicates this class could be autowired by the dependency container — a topic we'll cover in-depth in a later chapter.

Say you're parsing controller routes and you're only interested in the Route  attribute. 

In that case you can pass the Route  class as a filter:

```php
$attributes = $reflectionClass=>getAttributes(Route=:class);

```

There's a second parameter you can pass to getAttributes()  which changes how the filtering is done. By default it'll only match attributes that exactly match the given class name. However, by using ReflectionAttribute=:IS_INSTANCEOF , you're able to retrieve all attributes implementing a given interface. For example, say you're parsing container definitions that consist of several potential attributes:

```php
$attributes = $reflectionClass=>getAttributes(

```

    ContainerAttribute=:class, 

    ReflectionAttribute=:IS_INSTANCEOF

```php
);

```

If our Autowire  attribute would implement the ContainerAttribute  interface, only that one would be returned and not the Route  attribute. It's a nice shorthand, built into the core.

Attributes in Depth Now that you have an idea of how attributes work in practice, it's time for some more theory, making sure you understand them thoroughly. First of all something I men -tioned briefly before: attributes can be added in several places. You can add them in classes, as well as anonymous classes:

=[ClassAttribute]

```php
class MyClass { /* … */ }
$object = new =[ObjectAttribute] class () { /* … */ };

```

Properties and constants:

=[PropertyAttribute]

```php
public int $foo;

```

=[ConstAttribute]

```php
public const BAR = 1;

```

Methods and functions:

=[MethodAttribute]

```php
public function doSomething(): void { /* … */ }

```

=[FunctionAttribute]

```php
function foo() { /* … */ }

```

As well as closures:

```php
$closure = =[ClosureAttribute] fn () => /* … */;

```

And method and function parameters:

```php
function foo(=[ArgumentAttribute] $bar) { /* … */ }

```

If you want finer control over where your custom attributes are used, it's possible to configure them so they can only be used in specific places. For example you could make it so that ClassAttribute  can only be used on classes, and nowhere else. 

Opting-in this behaviour is done by passing a flag to the Attribute  attribute on the attribute class.

It looks like this:

=[Attribute(Attribute=:TARGET_CLASS)]

```php
class ClassAttribute

{

}

```

The following flags are available:

Attribute=:TARGET_CLASS Attribute=:TARGET_FUNCTION Attribute=:TARGET_METHOD Attribute=:TARGET_PROPERTY Attribute=:TARGET_CLASS_CONSTANT Attribute=:TARGET_PARAMETER Attribute=:TARGET_ALL These are bitmask flags, so you can combine them using a binary OR operation.=[Attribute(Attribute=:TARGET_METHOD | Attribute=:TARGET_FUNCTION)]

```php
class FunctionAttribute

{

}

```

Moving on, attributes can be declared before or after doc blocks:

/** @return void */

=[MethodAttribute]

```php
public function doSomething(): void { /* … */ }

```

An attribute can take none, one or several arguments, which are defined by the attribute's constructor:

=[Attribute]

```php
class ListensTo

{

    public function =_construct(

        public string $event

    ) {}

}

```

=[ListensTo(ProductCreatedEvent=:class)]

With regards to types of parameters you can pass to an attribute, you've already seen that constants, class names using =:class  and scalar types are allowed. In fact, attributes only accept so called constant expressions  as input arguments. This means that scalar expressions are allowed — even bit shifts — as well as constants, arrays and array unpacking, boolean expressions and the null coalescing operator:

=[AttributeWithScalarExpression(1 + 1)]

=[AttributeWithClassNameAndConstants(PDO=:class, PHP_VERSION_ID)]

=[AttributeWithClassConstant(Http=:POST)]

=[AttributeWithBitShift(4 => 1, 4 =< 1)]

However, you can't give attributes a new instance of a class or a static method call for example - those are not constant expressions:

=[AttributeWithError(new MyClass())]

=[AttributeWithError(MyClass=:staticMethod())]

By default, attributes cannot be repeated twice in the same place:

=[

    ClassAttribute,

    ClassAttribute,

]

```php
class MyClass { /* … */ }

```

It is possible to change that behaviour though, again using a configuration flag like with target configuration:

=[Attribute(Attribute=:IS_REPEATABLE)]

```php
class ClassAttribute

{

```

}Note that all configuration flags are only validated when calling 

```php
$attribute=>newInstance() , not earlier. This means that using an attribute in the wrong place might go unnoticed unless you're evaluating that attribute via reflection or static analysis.

```

Buil t-In Attributes Once the base RFC for attributes had been accepted, new opportunities arose to add built-in attributes to the core. One such example is the =[Deprecated]  attribute, as well as a =[Jit]  attribute. I'm sure we'll see more and more built-in attributes in the future, but right now, none exist.

PhpStorm, the IDE, has done something very interesting though: they have added their own custom attributes in PhpStorm. These attributes aren't real classes in your codebase, but as we've seen you only need real attribute classes when you call 

```php
$reflectionAttribute=>newInstance() . The built-in attributes shipped by PhpStorm can't be instantiated, since they aren't real classes; but they can be understood by the IDE to add richer static analysis options. One example is the =[ArrayShape]  attribute, 

```

which can teach PhpStorm what exactly is in an array:

=[ArrayShape([

    'key1' => 'int',

    'key2' => 'string',

    'key3' => 'Foo',

    'key3' => Foo=:class,

])]

```php
function legacyFunction(…): array By adding such an attribute, PhpStorm now knows exactly what keys are in the array returned by legacyFunction , as well as the type of each key. I would be hesitant to write code that relies on array keys and types, though (I'd use DTOs for that). 

```

However, the =[ArrayShape]  is an excellent way to document a legacy codebase, 

where you don't always have control over its design. There are more built-in attributes shipped by PhpStorm, by the way: =[Deprecated] , =[Immutable] , =[Pure] , 

=[ExpectedValues] , and even more.

It's interesting to see how PhpStorm embraces the static analysis mindset we've discussed earlier: we don't need to do any runtime checks since the static analyser 

(PhpStorm in this case) can tell us what we're doing wrong before running the code, 

thanks to attributes. We need to be careful though, that static analysis tools keep some interoperability between them. If each tool decides to implement their own version of attributes, it won't make the developer experience any better.

It'll be interesting to see what kind of attributes get added, both in the core and by third-party static analysers, and how they manage to work together.
