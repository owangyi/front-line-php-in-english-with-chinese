# 第十章

## MATCH

PHP 8 引入了新的 match 表达式——一个强大的功能，与使用 switch 相比，它通常是更好的选择。我说"通常"是因为 match 和 switch 都有对方无法覆盖的特定用例。那么到底有什么区别？让我们通过比较两者来开始。以下是一个经典的 switch 示例：

```php
switch ($statusCode) {

    case 200:

    case 300:
$message = null;

        break;

    case 400:
$message = 'not found';

        break;

    case 500:
$message = 'server error';

        break;

```

    default:

```php
$message = 'unknown status code';

        break;

```

}以下是它的 match 等价形式：

```php
$message = match ($statusCode) {

```

    200, 300 => null,

    400 => 'not found',

    500 => 'server error',

```php
    default => 'unknown status code',

};

```

首先，match 表达式明显更短：

```php
• it doesn't require a break  statement;

```

• it can combine different arms into one using a comma; and

• it returns a value, so you only have to assign the result once.

所以从语法角度来看，match 总是更容易编写。不过，还有更多差异。

## 表达式还是语句？

我称 match 为表达式，而 switch 是语句。两者之间确实有区别。表达式组合值和函数调用，

并被解释为一个新值。换句话说：它返回一个结果。这就是为什么我们可以将 match 的结果存储到变量中，而 switch 不可能做到这一点。

## 无类型强制转换

match 将进行严格的类型检查而不是宽松的类型检查。就像使用 === 而不是 ==。

但是，可能有些情况下你希望 PHP 自动处理变量的类型，这解释了为什么你不能用 match 替换所有 switch。

```php
$statusCode = '200';
$message = match ($statusCode) {

```

    200 => null default => 'Unknown status code',

```php
};

```

// $message = 'Unknown status code'

## 未知值会导致错误

当没有 default 分支并且传入的值不匹配任何给定选项时，PHP 将在运行时抛出 UnhandledMatchError。再次强调严格性，但这将防止细微的 bug 被忽视。

```php
$statusCode = 400;
$message = match ($statusCode) {

```

    200 => 'perfect',

```php
};

```

// UnhandledMatchError

## 目前仅支持单行表达式

就像短闭包一样，你只能编写一个表达式。表达式块可能会在某个时候添加，但具体时间仍不清楚。

## 组合条件

我已经提到了缺少 break；这也意味着 match 不允许穿透条件，就像第一个 switch 示例中的两个组合 case 行一样。

但是，另一方面，你可以在同一行上组合条件，用逗号分隔：

```php
$message = match ($statusCode) {

```

    200, 300, 301, 302 => 'combined expressions',

```php
};

```

## 复杂条件和性能

当 match RFC 被讨论时，一些人建议没有必要添加它，因为不使用额外的关键字而是依赖数组键已经可以实现相同的功能。以这个示例为例，我们想基于更复杂的正则表达式搜索来匹配值。在这里，我们使用一些人提到的作为 match 替代方案的数组表示法：

```php
$message = [
$this=>matchesRegex($line) => 'match A',
$this=>matchesOtherRegex($line) => 'match B',

][$search] =? 'no match';

```

但有一个很大的警告：这种技术会首先执行所有正则表达式函数来构建数组。另一方面，match 将逐个分支评估，这是更优化的方法。

## 抛出异常

最后，由于 PHP 8 中的 throw 表达式，如果你愿意，也可以直接从分支中抛出。

```php
$message = match ($statusCode) {

```

    200 => null,

    500 => throw new ServerError(),

```php
    default => 'unknown status code',

```

};

## 模式匹配

还有一个重要的功能仍然缺失：适当的模式匹配。这是其他编程语言中使用的一种技术，允许复杂的匹配规则而不是简单的比较。把它想象成正则表达式，但用于变量而不是文本。

模式匹配目前不受支持，因为它是一个相当复杂的功能。不过，它已被提及作为 match 的未来改进。我已经在期待它了！

## 那么，Switch 还是 Match？

如果我需要用一句话总结 match 表达式，我会说它是其小兄弟 switch 的更严格和更现代的版本。

有一些情况——看到我在那里做了什么吗？——switch 将提供更大的灵活性，特别是在多行代码块和其类型处理方面。另一方面，我发现 match 的严格性很有吸引力，模式匹配的前景对 PHP 来说将是一个改变游戏规则的功能。

我承认我过去从未写过 switch 语句，因为它有很多怪癖；match 实际上解决了这些怪癖。所以虽然它还不完美，但在某些用例中，match 会是一个很好的……匹配。

