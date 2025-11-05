# Chapter 9: Working with Arrays

I've already used some array-specific syntax in the previous chapters, so it seems like

我在前面的章节中已经使用了一些数组特定的语法，所以似乎应该花一些时间来专门讨论它们。现在不用担心：我不会讨论 PHP 中所有与数组相关的函数，它们太多了，这会相当无聊。不，我只讨论过去几年中数组和 PHP 语法使成为可能的内容。在处理数组时添加了很多好东西。我们将在本章中讨论所有这些。

a good idea to dedicate some time to them as well. Now don't worry: I won't discuss

你已经在之前的示例中看到了 `==.` 运算符的两种用法：你可以使用它来"展开"数组元素并将它们单独传递给函数，以及创建可变函数，将"剩余"参数收集到数组中。

all array-related functions in PHP, there are too many of them, which would be rather

让我们快速回顾一下。这里我们将数组元素展开到函数中：

boring. No, I'll only talk about what's made possible with arrays and PHP's syntax over

这里，我们使用可变函数，它收集剩余参数并将它们存储在数组中：

the last year. There have been quite a lot of niceties added when dealing with arrays.

在这种情况下，`$firstInput` 将是 `'a'`，而 `$listOfOthers` 将是一个数组：`['b', 'c', 'd']`。

We'll talk all about it in this chapter.

关于可变函数的一个有趣的事情是，你也可以为它们添加类型提示，所以你可以说传递给 `$listOfOthers` 的所有变量应该是，例如，字符串：

Rest and Spread

你也可以将两者结合起来。以下是一个通用的静态构造函数实现，适用于任何类。它被包装在 trait 中，这样你就可以在你想要的任何类中使用它：

You've already seen the two uses of the ==. operator in previous examples: you can

在这个示例中，我们接受可变数量的输入参数，然后再次将它们展开到构造函数中。这意味着，无论构造函数接受多少变量，我们都可以使用 `make` 将这些变量传递给它。以下是在实践中的样子：

use it to "spread" array elements and pass them individually to functions, as well as

关于数组展开还有一件事要提：该语法也可以用于组合数组：

make variadic functions that collect the "rest" of the arguments into an array.

这是一种合并两个数组的简写方式。不过有一个重要的注意事项：只有当输入数组只有数字键时才允许使用这种数组内展开语法——不允许文本键。

Let's quickly recap. Here we're spreading array elements into a function:

数组解构是将元素从数组中提取出来的操作——它是关于将数组"解构"为单独的变量。你可以使用 `list` 或 `[]` 来执行此操作。注意这个词是"destructure"（解构），而不是"destruction"（破坏）！

$data = ['a', 'b', 'c'];

以下是它的样子：

function handle($a, $b, $c): void { /* … */ }

无论你更喜欢 `list` 还是它的简写 `[]`，都由你决定。人们可能会争辩说 `[]` 与简写数组语法有歧义，因此更喜欢 `list`。我将在代码示例中使用简写版本，因为这是我的偏好。我认为由于 `[]` 符号在赋值运算符的左侧，很明显它不是数组定义。

handle(==.$data);

所以让我们看看使用这种语法可以做什么。

100

假设你只需要数组的第三个元素；前两个可以通过简单地不提供变量来跳过：

And here, we're using a variadic function, which collects the remaining parameters

还要注意，对具有数字索引的数组进行数组解构将始终从索引 0 开始。以下面的数组为例：

and stores them in an array.

提取的第一个变量将是 `null`，因为没有索引 0 的元素。这似乎是一个缺点，但幸运的是还有更多可能性。

function handle($firstInput, ==.$listOfOthers) { /* … */ }

PHP 7.1 允许数组解构用于具有非数字键的数组。这允许更大的灵活性：

handle('a', 'b', 'c', 'd');

如你所见，你可以按任何你想要的顺序排列，也可以完全跳过元素。

In this case, $firstInput will be 'a', while $listOfOthers will be an array:

数组解构的用途之一是与 `parse_url` 和 `pathinfo` 等函数一起使用。因为这些函数返回一个带有命名参数的数组，我们可以解构结果以提取我们想要的信息：

['b', 'c', 'd'].

你还可以在这个示例中看到，变量不需要与键同名。但是，如果你解构一个具有未知键的数组，PHP 会发出通知：

One interesting thing about variadic functions is that you can type hint them as well,

在这种情况下，`$query` 将是 `null`。你可以在示例中观察到最后一个细节：命名解构允许尾随逗号，就像你习惯使用数组一样。

so you can say that all variables passed into $listOfOthers should be, for example,

数组解构有更多用例——你已经在前面的属性章节中看到了这个用法。你可以在循环中解构数组：

strings:

这在解析时可能很有用，例如解析 JSON 或 CSV 文件。只是要小心，未定义的键仍然会触发通知。

function handle($firstInput, string ==.$listOfOthers) { /* … */ }

所以，这就是：你已经了解了在现代 PHP 中使用数组可以做的所有事情。我发现这些语法添加中的大多数都有它们的用例。总有不依赖简写的其他方法来实现相同的结果——这是你的选择。我们将在关于风格指南的章节中更多地讨论这些偏好，但首先还有一些其他主题要讨论。

You could also combine the two together. Here's a generic implementation of a static

constructor for any class. It's wrapped in a trait so that it can be used in whatever

class you want.

trait Makeable

{

public static function make(==.$args): static

{

return new static(==.$args);

}

}

In this example, we're taking a variable amount of input arguments and spreading

them again into the constructor. This means that, whatever amount of variables the

Chapter 09 - Working With Arrays

constructor takes, we can use make to pass those variables to it. Here's what that

would look like in practice:

class CustomerData

{

use Makeable;

public function =_construct(

public string $name,

public string $email,

public int $age,

) {}

}

$customerData = CustomerData=:make($name, $email, $age);

// Or you could use array spreading again:

$customerData = CustomerData=:make(==.$inputData);

One more thing to mention about array spreading: the syntax can be used to combine

arrays as well:

$inputA = ['a', 'b', 'c'];

$inputB = ['d', 'e', 'f'];

$combinedArray = [==.$inputA, ==.$inputB];

// ['a', 'b', 'c', 'd', 'e', 'f']

102

It's a shorthand way to merge two arrays. There's one important note, though: you're

only allowed to use this array-in-array-spreading syntax when the input arrays only

have numeric keys - textual keys aren't allowed.

Array Destructuring

Array destructuring is the act of pulling elements out of an array — it's about "de-

structuring" an array into separate variables. You can use both list or [] to do so.

Note that the word is "destructure", not "destruction"!

Here's what that looks like:

$array = [1, 2, 3];

// Using the list syntax:

list($a, $b, $c) = $array;

// Or the shorthand syntax:

[$a, $b, $c] = $array;

// $a = 1

// $b = 2

// $c = 3

Whether you prefer list or its shorthand [] is up to you. People might argue that []

is ambiguous with the shorthand array syntax and thus prefer list. I'll be using the

shorthand version in code samples as that is my preference. I think that since the []

Chapter 09 - Working With Arrays

notation is on the left side of the assignment operator, it's clear enough that it's not an

array definition.

So let's look at what's possible using this syntax.

Skipping Elements

Say you only need the third element of an array; the first two can be skipped by

simply not providing a variable.

[, , $c] = $array;

// $c = 3

Also note that array destructuring on arrays with numeric indices will always start at

index 0. Take for example the following array:

$array = [

1 => 'a',

2 => 'b',

3 => 'c',

];

The first variable pulled out would be null, because there's no element with index 0.

This might seem like a shortcoming, but luckily there are more possibilities.

104

Non-Numerical Keys

PHP 7.1 allows array destructuring to be used with arrays that have non-numerical

keys. This allows for more flexibility:

$array = [

'a' => 1,

'b' => 2,

'c' => 3,

];

['c' => $c, 'a' => $a] = $array;

As you can see, you can change the order however you want, and also skip elements

entirely.

In Practice

One of the uses of array destructuring are with functions like parse_url and pathinfo.

Because these functions return an array with named parameters, we can destructure

the result to pull out the information we'd like:

[

'basename' => $file,

'dirname' => $directory,

] = pathinfo('/users/test/file.png');

Chapter 09 - Working With Arrays

You can also see in this example that the variables don't need the same name as the

key. If you're destructuring an array with an unknown key however, PHP will issue a

notice:

[

'path' => $path,

'query' => $query,

] = parse_url('https:=/front-line-php.com');

// PHP Notice:  Undefined index: query

In this case, $query would be null. You could observe one last detail in the example:

trailing commas are allowed with named destructs, just like you're used to with arrays.

106

In Loops

Array destructuring has even more use cases — you've already seen this one used in

the attributes chapter. You can destructure arrays in loops:

$array = [

[

'name' => 'a',

'id' => 1

],

[

'name' => 'b',

'id' => 2

],

];

foreach ($array as ['id' => $id, 'name' => $name]) {

// …

}

This could be useful when parsing, for example, a JSON or CSV file. Only be careful

that undefined keys will still trigger a notice.

So there we have it: you're up to date with everything you can do using arrays in

modern-day PHP. I find that most of these syntactical additions have their use cases.

There are always other ways to achieve the same result that don't rely on shorthands

- it's your choice. We'll talk more about these kinds of preferences in the chapter on

style guides, but there are a few other topics to discuss first.

