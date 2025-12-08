# 第八章

## 短闭包

有些人可能认为它们早就应该有了，终于在 PHP 7.4 中得到了支持：

短闭包。与其编写像这样作为 array_map 回调传递的闭包：

```php
$itemPrices = array_map(

    function (OrderLine $orderLine) {

        return $orderLine=>item=>price;

```

    }, 

```php
$order=>lines

);

```

你可以用简短的形式编写它们：

```php
$itemPrices = array_map(

```

    fn ($orderLine) => $orderLine=>item=>price,

```php
$order=>lines

);

```

短闭包与普通闭包在两个方面有所不同：

• 它们只支持一个表达式，这也是返回语句；以及

• 它们不需要 use 语句来访问外部作用域的变量

关于其他一切，它们的行为就像普通闭包一样：它们支持引用、参数展开、类型提示、返回类型……说到类型，你可以用更严格的类型方式重写前面的示例，像这样：

```php
$itemPrices = array_map(

```

    fn (OrderLine $orderLine): int => $orderLine=>item=>price,

```php
$order=>lines

);

```

还有一件事，引用也是允许的，既用于参数也用于返回值。如果你想通过引用返回值，应该使用以下语法：

fn&($x) => $x

## 不支持多行

你可能已经注意到了：短闭包只能有一个表达式；它可能为了格式化而跨越多行，但它必须始终是一个表达式。推理如下：短闭包的目标是减少冗长。fn 当然在所有情况下都比 function 短。然而，有人认为，如果你正在处理多行函数，使用短闭包的好处就会减少。

毕竟，多行闭包根据定义已经更加冗长；所以能够跳过两个关键字（function 和 return）不会有太大区别。

虽然我能想到我的项目中有很多单行闭包，但也有大量的多行闭包，我承认在这些情况下缺少短语法。不过，有希望：

将来可能会添加多行短闭包，但我们还需要再等一段时间。

## 外部作用域的值

短闭包和普通闭包之间的另一个显著区别是，短闭包不需要 use 关键字就能访问外部作用域的数据：

```php
$modifier = 5;

array_map(fn ($x) => $x * $modifier, $numbers);

```

重要的是要注意，你将无法修改来自该外部作用域的变量：

它们按值绑定而不是按引用绑定，除非你正在处理总是按引用传递的对象。顺便说一下，这是对象在任何地方的默认行为，而不仅仅是在短闭包中。

当然，一个例外是 $this 关键字，它的行为与普通闭包完全相同：

```php
array_map(fn ($x) => $x * $this=>modifier, $numbers);

```

说到 $this，你可以将短闭包声明为 static，这意味着你将无法在其中访问 $this：

```php
static fn ($x) => $x * $this=>modifier;

```

// Fatal error: Uncaught Error: Using $this when not in object context 这就是目前关于短闭包要说的全部内容。你可以想象还有改进的空间。人们一直在谈论多行短闭包以及能够将语法用于类方法。我们将不得不等待未来的版本，看看短闭包是否以及如何发展。

