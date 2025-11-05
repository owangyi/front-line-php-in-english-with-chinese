# Chapter 6: Named Arguments

Just like constructor property promotion, named arguments are a new syntactical ad-

就像构造函数属性提升一样，命名参数是 PHP 8 中的一个新语法特性。它们允许你根据函数中的参数名称传递变量，而不是根据它们在参数列表中的位置。以下是一个使用内置 PHP 函数的示例：

dition in PHP 8. They allow you to pass variables to a function based on the argument

以及用于构造 DTO 的示例：

name in that function, instead of their position in the argument list. Here's an example

命名参数是一个很棒的新特性，将对我日常编程产生重大影响。你可能想知道细节。如果你传递了错误的名称会怎样？或者如何组合有序参数和命名参数？让我们深入探讨所有这些问题。

with a built-in PHP function:

这个特性是一个备受争议的特性。有人对添加它们表示担忧，特别是关于向后兼容性。如果你维护一个包并决定更改参数名称，这现在算作破坏性更改。以这个包提供的方法签名为例：

setcookie(

如果这个包的用户使用命名参数，他们会写类似这样的代码：

name: 'test',

现在想象一下，作为包维护者，你想将 `$collection` 的名称更改为 `$collectionName`。这意味着用户编写的代码会中断。

expires: time() + 60 * 60 * 2,

我同意这在理论上是问题，但作为开源维护者，我从经验中知道这种变量名称更改很少发生。我能记得我们进行这种更改的唯一几次是因为我们正在开发新的主要版本，允许破坏性更改。

secure: true,

虽然我认识到这个理论问题，但我坚信在实践中这不是问题。这种名称更改很少发生。即使你作为开源维护者真的不想被管理变量名称所困扰，你仍然可以在包的 README 文件中添加警告。它可以告诉用户变量名称可能会更改，他们应该自行承担使用命名参数的风险。我更喜欢只是记住它，并记住将来更改变量名称时应该小心。没什么大不了的。

);

尽管有这个小的不便，我认为命名参数的好处要重要得多。在我看来：命名参数将允许我们编写更清晰、更灵活的代码。

66

首先，命名参数允许我们跳过默认值。再看一下 cookie 示例：

And here's it used when constructing a DTO:

它的方法签名实际上是：

class CustomerData

在使用命名参数的示例中，我们不需要设置 cookie 的 `$value`，但我们确实需要设置过期时间。命名参数使这个方法调用更加简洁，因为否则它看起来会是这样：

{

除了跳过具有默认值的参数外，还有澄清哪个变量做什么的好处，这对于具有大方法签名的函数特别有用。我们可以说很多参数通常是代码异味；无论如何，我们仍然必须处理它们。所以有一个好的方法总比没有好。

public function =_construct(

让我们看看命名参数可以做什么和不能做什么。

public string $name,

首先，它们可以与未命名（也称为有序）参数组合使用。在这种情况下，有序参数必须始终放在前面。以我们之前的 DTO 示例为例：

public string $email,

你可以这样构造它：

public int $age,

但是，在命名参数之后使用有序参数会抛出错误：

) {}

其次，可以将数组展开与命名参数结合使用：

}

**注意！**

$data = new CustomerData(

就像可变函数一样，可以使用 `==.` 运算符展开数组。我们将从输入数组中获取所有参数并将它们展开到函数中。如果数组包含键值，这些键名也会映射到命名属性，这就是上面示例中发生的情况。

age: $input['age'],

但是，如果数组中缺少必需的条目，或者有一个未列为命名参数的键，则会抛出错误：

email: $input['email'],

可以在输入数组中组合命名参数和有序参数，但前提是有序参数遵循与之前相同的规则：它们必须放在前面！

name: $input['name'],

不过，混合使用有序参数和命名参数时要小心。我个人认为它们根本不会提高可读性。

);

如果你使用可变函数，命名参数将以其键名传递到可变参数数组中。看以下示例：

Named arguments are a great new feature and will have a significant impact on my

day-to-day programming life. You're probably wondering about the details. What if

you pass a wrong name, or what about combining ordered and named arguments?

Well, let's look at all those questions in-depth.

Why named arguments?

This feature was a highly debated one. There were some concerns about adding

them, especially with regards to backwards compatibility. If you're maintaining a

Chapter 06 - Named Arguments

package and decide to change an argument's name, this now counts as a breaking

change. Take for example this method signature, provided by a package:

public function toMediaCollection(

string $collection,

string $disk = null

): void { /* … */ }

If the users of this package would use named arguments, they write something like

this:

$media=>toMediaCollection(

collection: 'default',

disk: 'aws',

);

Now imagine you, the package maintainer, want to change the name of $collection

to $collectionName. This means the code written by your users would break.

I agree this is a problem in theory, but being an open source maintainer myself, I know

from experience that such variable name changes very rarely occur. The only times

I can remember that we did such a change was because we were working on a new

major release anyway, where breaking changes are allowed.

While I recognise the theoretical problem, I firmly believe this is a non-issue in prac-

tice. Such name changes rarely happen. And even if you really wouldn't want to be

bothered with managing variable names as an open source maintainer, you could still

add a warning in your package's README file. It could tell your users that variable

names might change, and they should use named arguments at their own risk. I prefer

just to keep it in mind, and remember that I should be careful changing variable names

in the future. No big deal.

68

Despite this minor inconvenience, I'd say the benefits of named arguments are far

more significant. The way I see it: named arguments will allow us to write cleaner and

more flexible code.

For one, named arguments allow us to skip default values. Take a look again at the

cookie example:

setcookie(

name: 'test',

expires: time() + 60 * 60 * 2,

secure: true,

);

Its method signature is actually the following:

setcookie(

string $name,

string $value = '',

int $expires = 0,

string $path = '',

string $domain = '',

bool $secure = false,

bool $httponly = false,

) : bool

Chapter 06 - Named Arguments

In the example with named arguments, we didn't need to set a cookie $value, but we

did need to set an expiration time. Named arguments made this method call a little

more concise, because otherwise it would have looked like this:

setcookie(

'test',

'',

time() + 60 * 60 * 2,

'',

'',

true

);

Besides skipping arguments with default values, there's also the benefit of clarifying

which variable does what, something that's especially useful in functions with large

method signatures. We could say that lots of arguments are usually a code smell; we

still have to deal with them no matter what. So it's better to have a good way of doing

so than nothing at all.

Named Arguments in Depth

Let's look at what named arguments can and cannot do with the basics out of the

way.

70

First of all, they can be combined with unnamed — also called ordered — arguments.

In that case, the ordered arguments must always come first. Take our DTO example

from before:

class CustomerData

{

public function =_construct(

public string $name,

public string $email,

public int $age,

) {}

}

You could construct it like so:

$data = new CustomerData(

$input['name'],

age: $input['age'],

email: $input['email'],

);

However, having an ordered argument after a named one would throw an error:

$data = new CustomerData(

age: $input['age'],

$input['name'],

email: $input['email'],

);

Chapter 06 - Named Arguments

Next, it's possible to use array spreading in combination with named arguments:

$input = [

'age' => 25,

'name' => 'Brent',

'email' => 'brent@spatie.be',

];

$data = new CustomerData(==.$input);

Heads up!

Just like with variadic functions, arrays can be spread using the ==. operator.

We'll take all arguments from the input array and spread them into a function. If

the array contains keyed values, those key names will map onto named proper-

ties as well, and that is what's happening in the above example.

If, however, there are missing required entries in the array, or if there's a key not listed

as a named argument, an error will be thrown:

$input = [

'age' => 25,

'name' => 'Brent',

'email' => 'brent@spatie.be',

'unknownProperty' => 'This is not allowed',

];

$data = new CustomerData(==.$input);

72

It is possible to combine named and ordered arguments in an input array, but only if

the ordered arguments follow the same rule as before: they must come first!

$input = [

'Brent',

'age' => 25,

'email' => 'brent@spatie.be',

];

$data = new CustomerData(==.$input);

Be careful mixing ordered and named arguments though. I personally don't think they

improve readability at all.

Chapter 06 - Named Arguments

Variadic Functions

If you're using variadic functions, named arguments will be passed with their key

name into the variadic arguments array. Take the following example:

class CustomerData

{

public static function new(==.$args): self

{

return new self(==.$args);

}

public function =_construct(

public string $name,

public string $email,

public int $age,

) {}

}

$data = CustomerData=:new(

email: 'brent@spatie.be',

age: 25,

name: 'Brent',

);

// [

//     'age' => 25,

//     'email' => 'brent@spatie.be',

//     'name' => 'Brent',

// ]

74

Attributes

Here we are again with the mysterious attributes feature - we'll cover them in depth

soon! For now, I can tell you that they also support named arguments when construct-

ing them:

class ProductSubscriber

{

=[ListensTo(event: ProductCreated=:class)]

public function onProductCreated(ProductCreated $event) { /* … */ }

}

Other Things Worth Noting

It's not possible to have a variable as the argument name:

$field = 'age';

$data = CustomerData=:new(

$field: 25,

);

Chapter 06 - Named Arguments

And finally, named arguments will deal in a pragmatic way with name changes during

inheritance. Take this example:

interface EventListener {

public function on($event, $handler);

}

class MyListener implements EventListener

{

public function on($myEvent, $myHandler)

{

// …

}

}

PHP will silently allow changing the name of $event to $myEvent, and $handler to

$myHandler; but if you decide to use named arguments using the parent's name, it will

result in a runtime error:

public function register(EventListener $listener)

{

$listener=>on(

event: $this=>event,

handler: $this=>handler,

);

}

This pragmatic approach was chosen to prevent a major breaking change where all

inherited arguments would have to keep the same name. It seems like an excellent

solution to me. You can expect to see named arguments used in this book here and

there. I think they are great syntactical sugar.

76

