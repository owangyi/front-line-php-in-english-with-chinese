# 第十一章

## 面向对象的 PHP

现在你已经掌握了现代 PHP 语法，是时候更深入地看看我们用它编写什么样的代码了。在接下来的章节中，我们将放大视野来看更大的图景。我们将从一个备受争议的话题开始：面向对象编程。

"面向对象编程"这个术语的发明者 Alan Kay，在 20 多年前的一次演讲中讲过一个故事。你可以只用锤子、钉子、木板和一点点技能来建造一个狗屋。我想即使是我，只要有足够的时间也能建造它。一旦你建造了它，你就获得了技能和知识，可以将其应用到其他项目中。接下来，你想建造一座大教堂，使用相同的方法，用你的锤子、钉子和木板。它大了 100 倍，但你以前做过这个——对吧？只需要更长一点时间。

虽然规模增加了 100 倍，但它的质量增加了 1,000,000 倍，而它的强度只增加了 10,000 倍。不可避免地，建筑会倒塌。有些人用灰泥覆盖废墟，把它做成金字塔，说这本来就是计划；但你我都知道真正发生了什么。

你可以在这里观看 Alan 的演讲：https://www.youtube.com/watch?v=oKg1h-TOQXoY

Alan 用这个比喻来解释他在 20 年前看到的"现代 OOP"的一个关键问题。我认为它今天仍然适用：我们采用了问题的解决方案——OO 代码

——我们将其扩大了 100 倍，并期望它以相同的方式工作。即使在今天，我们对架构的思考也不够——如果你正在建造一座大教堂，这是相当关键的——我们使用我们学到的 OO 解决方案，没有任何额外的思考。

我们大多数人都是在孤立的情况下学习 OO，使用小例子，很少在规模上学习。在大多数实际项目中，你不能简单地应用你学到的模式，并期望一切都像使用 Animals、Cats 和 Dogs 那样顺利。

这种对 OO 代码的鲁莽扩展导致许多人在最近几年表达了对它的不满。我认为 OOP 和其他工具一样好——函数式编程是当今流行的竞争者——如果使用正确的话。

我从 Alan 20 年前的演讲中得到的启示是，每个对象本身都是一个小程序，有自己的内部状态。对象之间相互发送消息——包

含不可变数据的包——其他对象可以解释并对其做出反应。你不能以这种方式编写所有代码，这是可以接受的——不盲目遵循这些规则是可以的。尽管如此，我亲身体验了这种思维方式的积极影响。将对象视为独立的小程序，我开始以不同的方式编写部分代码

风格。我希望，现在我们要看面向对象的 PHP，你会记住 Alan 的想法。它们教会我批判性地看待我认为理所当然的

"适当的 OO"，并了解到它比你想象的更多。

## OOP 的替代方案

我不想在这本书中推广任何隧道视野。我知道除了 OOP 之外，还有其他编程方法。例如，函数式编程在最近几年中获得了巨大的流行。虽然我认为 FP 有其优点，但 PHP 并没有针对函数式风格进行优化。另一方面，虽然 OOP 是 PHP 的最佳匹配，但所有程序员都可以通过学习其他编程风格（如函数式风格）来学习宝贵的经验。

我建议你阅读 Larry Garfield 写的一本名为"Thinking Functionally in PHP"的书。在书中，Larry 清楚地展示了为什么 PHP 不是编写函数式程序的完美语言，但他也用 PHP 解释了 FP 的思维方式。即使你不会编写函数式 PHP 生产代码，

也有很多知识我们可以应用到 OOP 中。

## 继承的陷阱

我最初觉得很难相信，但类和继承与 Alan 设想的 OOP 方式无关。这并不意味着它们本身是坏事，

但思考它们的目的以及我们如何使用（以及滥用）它们是有好处的。

Alan 的愿景只描述了对象——它没有解释这些对象是如何创建的。类后来被添加为管理对象的便捷方式，但它们只是一个实现细节，不是 OOP 的核心思想。随着类的出现，继承也出现了，

另一个在正确使用时很有用的工具。不过，情况并非总是如此。

即使你可能认为它是面向对象设计的支柱之一，它们也经常被滥用，就像 Alan 试图将狗屋扩大到教堂一样。

OOP 的一个公认优势是它以人类思考世界的方式对我们的代码进行建模。但在现实中，我们很少从抽象和继承的角度思考。

我们没有在真正有意义的地方使用继承，而是滥用它来共享代码，并以一种模糊的方式配置对象。我将向你展示一个很好的例子来说明这个问题，尽管我想提前说明这不是我自己的：它是 Sandi Metz 的，一位关于 OOP 主题的优秀教师。让我们来看看。

Sandi 的演讲：https://www.youtube.com/watch?v=OMPfEXIlTVE有一首儿童童谣叫" The House That Jack Built"（它也是一部恐怖电影，但那是无关的）。它开始是这样的：

这是 Jack 建造的房子。

每次迭代，都会添加一个句子：

这是放在 Jack 建造的房子里的麦芽。

接下来这是吃了放在 Jack 建造的房子里的麦芽的老鼠。

明白了吗？这是最终的诗：

这是属于播种玉米的农民的，养了在早晨啼叫的公鸡的，叫醒了剃光胡子的牧师的，嫁给了衣衫褴褛的男人的，亲吻了孤独的少女的，挤了有皱角的奶牛的，扔了担心猫的狗的，杀了吃了放在 Jack 建造的房子里的麦芽的老鼠的猫的马、猎犬和号角。

让我们用 PHP 编写这个：一个程序，你可以询问给定的迭代，它会生成到该点的诗。让我们以 OO 的方式来做。我们首先将所有部分添加到类中的数据数组中；让我们称该类为 PoemGenerator——听起来很 OO，

对吧？好的。

```php
class PoemGenerator

{

    private static array $data = [

```

        'the horse and the hound and the horn that belonged to',

        'the farmer sowing his corn that kept',

        'the rooster that crowed in the morn that woke',

        'the priest all shaven and shorn that married',

        'the man all tattered and torn that kissed',

        'the maiden all forlorn that milked',

        'the cow with the crumpled horn that tossed',

        'the dog that worried','the cat that killed',

        'the rat that ate',

        'the malt that lay in',

        'the house that Jack built',

```php
    ];

}

```

现在让我们添加两个方法 generate 和 phrase。generate 将返回最终结果，

phrase 是一个将部分粘合在一起的内部函数。

```php
class PoemGenerator

{

```

    // …

```php
    public function generate(int $number): string

    {

        return "This is {$this=>phrase($number)}.";

    }

    protected function phrase(int $number): string

    {
$parts = array_slice(self=:$data, -$number, $number);

        return implode("\n        ", $parts);

    }

}

```

看起来我们的解决方案有效：我们可以使用 phrase 从数据数组的末尾获取 x 数量的项目，并将它们合并成一个短语。接下来，我们使用 generate 用 This is 和 . 包装最终结果。顺便说一下，我在那个空格分隔符上使用 implode 只是为了稍微格式化输出。

```php
$generator = new PoemGenerator();
$generator=>generate(4);

```

// This is the cat that killed

//         the rat that ate

//         the malt that lay in

//         the house that Jack built.

正是我们期望的结果。

然后出现了……一个新的功能请求。让我们构建一个随机诗歌生成器：它将随机化短语的顺序。我们如何在不复制和重复代码的情况下以干净的方式解决这个问题？继承来救援——对吧？首先，让我们做一个小重构：让我们添加一个受保护的 data 方法，这样我们在它实际返回的内容上有更多的灵活性：

```php
class PoemGenerator 

{

    protected function phrase(int $number): string

    {
$parts = array_slice($this=>data(), -$number, $number);

        return implode("\n        ", $parts);

    }

    protected function data(): array

    {

        return [

```

            'the horse and the hound and the horn that belonged to',

            // …

            'the house that Jack built',

```php
        ];

    }

}

```

接下来我们构建我们的 RandomPoemGenerator：

```php
class RandomPoemGenerator extends PoemGenerator

{

    protected function data(): array

    {
$data = parent=:data();

        shuffle($data);

        return $data;

    }

}

```

继承有多棒！我们只需要覆盖代码的一小部分，一切都能按预期工作！

```php
$generator = new RandomPoemGenerator();
$generator=>generate(4);

```

// This is the priest all shaven and shorn that married

//         the cow with the crumpled horn that tossed

//         the man all tattered and torn that kissed

//         the rooster that crowed in the morn that woke.

太棒了！再一次……一个新的功能请求：一个回声生成器：它重复每一行第二次。所以你会得到这个：

这是放在 Jack 建造的房子里的麦芽，放在 Jack 建造的房子里的麦芽，Jack 建造的房子，Jack 建造的房子。

我们可以解决这个问题；继承——对吧？

让我们再次在 PoemGenerator 中进行小重构，只是为了确保我们的代码保持干净。我们可以将 phrase 中的数组切片功能提取到它自己的方法中，这似乎是更好的关注点分离。

```php
class PoemGenerator

{

```

    // …

```php
    protected function phrase(int $number): string

    {
$parts = $this=>parts($number);

        return implode("\n        ", $parts);

    }

    protected function parts(int $number): array

    {

        return array_slice($this=>data(), -$number, $number);

    }

}

```

重构后，实现 EchoPoemGenerator 再次变得非常容易：

```php
class EchoPoemGenerator extends PoemGenerator

{

    protected function parts(int $number): array

    {

        return array_reduce(

```

            parent=:parts($number),

            fn (array $output, string $line) => 

                [==.$output, "{$line} {$line}"],

            []

```php
        );

    }

}

```

我们能否花点时间欣赏继承的力量？我们已经创建了原始 PoemGenerator 的两个不同实现，并且只在 RandomPoemGenerator 和 EchoPoemGenerator 中覆盖了与它不同的部分。我们甚至使用了 SOLID 原则（或者我们这样认为）来确保我们的代码是解耦的，以便轻松覆盖特定部分。这就是伟大的 OOP 的意义所在——对吧？

再一次……另一个功能请求：请再做一个实现，一个结合了随机和回声行为的实现：RandomEchoPoemGenerator。

现在怎么办？那个类将扩展哪个类？

如果我们扩展 PoemGenerator，我们将不得不覆盖我们的 data 和 parts 方法，基本上从 RandomPoemGenerator 和 EchoPoemGenerator 复制代码。这是糟糕的设计，到处复制代码。如果我们扩展 RandomPoemGenerator 呢？我们需要从 EchoPoemGenerator 重新实现 parts。如果我们实现 EchoPoemGenerator，情况会相反。

老实说，扩展 PoemGenerator 并复制两个实现似乎是最好的解决方案。因为这样，我们至少向未来的程序员明确表示这是它自己的东西，我们无法以任何其他方式解决它。

但让我们坦率地说：无论什么解决方案，都是垃圾。我们陷入了继承的陷阱。亲爱的读者，这在现实项目中经常发生：我们认为继承是覆盖和重用行为的完美解决方案，它一开始总是看起来很棒。接下来出现了一个新功能，导致更多抽象，并导致我们的代码失控。我们认为我们掌握了继承，但它反而踢了我们的屁股。

那么问题是什么——我们代码的实际问题是什么？RandomPoemGenerator 从 PoemGenerator 扩展不是有意义的吗？它是一个诗歌生成器，不是吗？这确实是我们思考继承的方式：使用"是一个"。是的，

RandomPoemGenerator 是一个 PoemGenerator，但 RandomPoemGenerator 现在不只是生成诗歌，不是吗？

Sandi Metz 建议用以下问题来识别潜在问题："两者之间发生了什么变化——继承期间发生了什么变化？"嗯……在 RandomPoemGenerator 的情况下，是 data 方法；对于 EchoPoemGenerator，是 parts 方法。恰好需要组合这两个部分使我们的继承解决方案爆炸了。

你知道这意味着什么吗？这意味着 parts 和 data 本身就是某种东西。它们不仅仅是我们的诗歌生成器的受保护实现细节。

它们是客户所重视的，它们是我们程序的本质。

所以让我们这样对待它们。

确定了两个独立的关注点，我们需要给它们一个合适的名称。第一个是关于行是否应该随机化。让我们称它为 Orderer；它将接受一个原始数组并返回一个新版本，其项目按特定方式排序。

```php
interface Orderer

{

    public function order(array $data): array;

}

```

第二个关注点是关于格式化输出——是否应该回显。让我们称这个概念为 Formatter。它的任务是接收行数组并将所有这些行格式化为一个字符串。

```php
interface Formatter

{

    public function format(array $lines): string;

```

}这就是魔法所在。我们正在从 PoemGenerator 中提取这个逻辑，但我们仍然需要一种从内部访问它的方法。所以让我们将一个 orderer 和 formatter 注入到 PoemGenerator 中：

```php
class PoemGenerator

{

    public function =_construct(

        public Formatter $formatter,

        public Orderer $orderer,

    ) {}

    

```

    // …

```php
}

```

有了两者，让我们更改 phrase 和 data 的实现细节：

```php
class PoemGenerator

{

```

    // …

```php
    protected function phrase(int $number): string

    {
$parts = $this=>parts($number);

        return $this=>formatter=>format($parts);

    }

    protected function data(): array

    {

        return $this=>orderer=>order([

```

            'the horse and the hound and the horn that belonged to',

            // …

            'the house that Jack built',

```php
        ]);

    }

```

}最后，让我们实现 Orderer：

```php
class SequentialOrderer implements Orderer

{

    public function order(array $data): array

    {

        return $data;

    }

}

class RandomOrderer implements Orderer

{

    public function order(array $data): array

    {

        shuffle($data);

        return $data;

    }

}

```

以及 Formatter：

```php
class DefaultFormatter implements Formatter

{

    public function format(array $lines): string

    {

        return implode("\n        ", $lines);

    }

}

class EchoFormatter implements Formatter

{

    public function format(array $lines): string

    {
$lines = array_reduce(
$lines,

```

            fn (array $output, string $line) => 

                [==.$output, "{$line} {$line}"],

            []

```php
        );

        return implode("\n        ", $lines);

    }

}

```

默认实现 DefaultFormatter 和 SequentialOrderer 可能不会执行任何复杂的操作，但它们仍然是有效的业务关注点："顺序

顺序"和"默认格式"是创建我们以正常形式所知的诗歌所需的两个有效案例。

你意识到刚才发生了什么吗？你可能认为我们正在编写更多代码，但你忘记了什么……我们可以完全删除我们的 RandomPoemGenerator 和 EchoPoemGenerator，我们不再需要它们了，我们可以只用 PoemGenerator 解决所有情况：

```php
$generator = new PoemGenerator(

    new EchoFormatter(), 

    new RandomOrderer(),

);

```

我们可以通过提供适当的默认值来使我们的生活更轻松一些：

```php
class PoemGenerator

{

    public function =_construct(

        public ?Formatter $formatter = null,

        public ?Orderer $orderer = null,

    ) {
$this=>formatter =?= new DefaultFormatter();
$this=>orderer =?= new SequentialOrderer();

    }

}

```

使用命名属性，我们可以以任何我们想要的方式构造 PoemGenerator：

```php
$generator = new PoemGenerator(

```

    formatter: new EchoFormatter(), 

```php
);
$generator = new PoemGenerator(

```

    orderer: new RandomOrderer(), 

```php
);
$generator = new PoemGenerator(

```

    formatter: new EchoFormatter(), 

    orderer: new RandomOrderer(), 

```php
);

```

不再需要第三个抽象！

这是真正的面向对象编程。我告诉过你 OOP 不是关于继承的，

这个例子显示了它的真正力量。通过将对象组合成其他对象，

我们能够创建一个灵活且持久的解决方案，一个以干净的方式解决我们所有问题的方案。这就是组合优于继承的意义，它是 OO 中最基本的支柱之一。

我承认：我在开始编写代码时并不总是使用这种方法。在开发过程中，通常更容易简单地开始，而不考虑抽象或组合。我甚至会说这是一个很好的规则：不要太早抽象。重要的教训不是你应该总是使用组合。相反，它是关于识别你遇到的问题并使用正确的解决方案来解决它。

那么 traits 呢？

你可能正在考虑使用 traits 来解决我们的诗歌问题。你可以创建一个 RandomPoemTrait 和 EchoPoemTrait，实现 data 和 phrase。是的，traits 可以是另一个解决方案，就像继承也是一个可行的解决方案一样。我将说明为什么组合仍然是更好的选择，但首先让我们在实践中展示这些 traits 会是什么样子：

```php
trait RandomPoemTrait

{

    protected function data(): array

    {
$data = parent=:data();

        shuffle($data);

        return $data;

    }

}

trait EchoPoemTrait

{

    protected function parts(int $number): array

    {

        return array_reduce(

```

            parent=:parts($number),

            fn (array $output, string $line) => 

                [==.$output, "{$line} {$line}"],

            []

```php
        );

    }

}

```

你可以使用这些来实现 RandomEchoPoemGenerator，像这样：

```php
class RandomEchoPoemGenerator extends PoemGenerator

{

    use RandomPoemTrait;

    use EchoPoemTrait;

}

```

Traits 确实解决了代码可重用性的问题；这正是它们被添加到语言中的原因。当我提到添加 RandomEchoPoemGenerator 的最新功能请求时，我评论说没有干净的方法来解决这个问题而不进行代码重复，这是寻找另一个解决方案——组合——的垫脚石。我是否故意忽略 traits 来证明我的观点？不。虽然它们确实解决了可重用性问题，但它们没有我们在探索组合时发现的额外好处。

首先，我们发现诗歌的顺序和格式是关键的业务规则，不应该被视为类中某处的受保护实现细节。我们创建了 Orderer 和 Formatter 来使我们的代码更好地表示我们试图解决的实际问题。如果我们选择 traits 和子类，我们会再次失去这种明确性。

其次，我们的诗歌示例显示了 PoemGenerator 的两个可配置部分。如果有三个或四个呢？如果我们添加两个更多的 traits，我们还必须为这些 traits 创建新的子类实现，以及与现有 traits 的所有相关组合。子类的数量将呈指数增长。即使在我们当前的示例中，已经有三个子类：RandomPoemGenerator、

EchoPoemGenerator 和 RandomEchoPoemGenerator。另一方面，组合只要求我们只添加两个新类。如果有更复杂的业务规则需要考虑，我们的代码会失控。

我不是建议根本不应该使用 traits；就像继承一样，它们有它们的用途。最重要的是，你要批判性地评估所有解决方案的优缺点

对于给定问题，而不是回到最初看起来最容易的方法。

我认为这种推理适用于所有与编程相关的事情，无论你是在面向对象、过程式还是函数式风格中编码。OOP 得到了一个坏名声，因为人们开始失控地扩展它，而没有重新思考他们的架构。我希望我们能改变这一点。

