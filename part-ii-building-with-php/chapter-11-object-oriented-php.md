# Chapter 11: Object Oriented PHP

Now that you're up to speed with modern PHP syntax, it's time to look deeper into

现在你已经掌握了现代 PHP 语法，是时候深入了解我们用它编写什么样的代码了。在接下来的几章中，我们将放大视野，看到更大的图景。我们将从一个备受争议的话题开始：面向对象编程。

what kind of code we write with it. throughout the next chapters, we'll zoom out to

Alan Kay，"面向对象编程"这个术语的发明者，在20多年前的一次演讲中讲了一个故事。你可以只用锤子、钉子和木板，再加上一点技能来建造一个狗屋。我认为即使是我，只要有足够的时间也能建造它。一旦你建造了它，你就获得了技能和知识，可以将其应用到其他项目中。接下来，你想用同样的方法建造一座大教堂，使用你的锤子、钉子和木板。它大了100倍，但你以前做过这个——对吧？只需要再长一点时间。

see the bigger picture. We'll start with a heavily debated topic: object-oriented pro-

虽然规模增加了100倍，但它的质量增加了1,000,000倍，而强度只增加了10,000倍。不可避免地，建筑会倒塌。有些人把碎石抹上灰泥，做成金字塔，说这本来就是计划；但你我知道真正发生了什么。

gramming.

你可以在这里观看 Alan 的演讲：https://www.youtube.com/watch?v=oKg1h-TOQXoY

Alan Kay, the inventor of the term "object-oriented programming", told a story once

Alan 用这个比喻来解释他在20年前看到的"现代 OOP"的一个关键问题。我认为今天仍然适用：我们把一个问题的解决方案——OO代码——扩大了100倍，期望它能以同样的方式工作。即使在今天，我们也没有足够地思考架构——如果你要建造大教堂，这是相当关键的——我们使用我们学到的 OO 解决方案，没有额外的思考。

during a talk more than 20 years ago. You can build a dog house using only a hammer,

我们大多数人都是在孤立的情况下学习 OO，使用小例子，很少在大规模情况下学习。在大多数现实项目中，你不能简单地应用你学到的模式，期望一切都能像 Animals、Cats 和 Dogs 那样顺利。

nails, planks, and just a little bit of skill. I figure even I would be able to build it given

这种鲁莽的 OO 代码扩展导致许多人在最近几年表达了他们的反对意见。我认为 OOP 和任何其他工具一样好——函数式编程是当今流行的竞争者——如果使用正确的话。

enough time. Once you've built it you've earned the skills and know-how, and could

我从 Alan 20年前的演讲中得到的启示是，每个对象都是一个独立的小程序，有自己的内部状态。对象之间相互发送消息——不可变数据包——其他对象可以解释并做出反应。你不能用这种方式编写所有代码，这是可以接受的——不盲目遵循这些规则是可以的。尽管如此，我亲身经历了这种思维方式的积极影响。将对象视为独立的小程序，我开始以不同的风格编写代码的一部分。我希望，现在我们要看面向对象的 PHP 时，你会记住 Alan 的想法。它们教会我批判性地看待我认为理所当然的"正确的 OO"，并了解到它的内容比你想象的要多。

apply it to other projects. Next, you want to build a cathedral, using the same ap-

我不想在这本书中推广任何隧道视野。我知道除了 OOP 之外还有其他编程方法。例如，函数式编程在最近几年中看到了巨大的流行度增长。虽然我认为 FP 有其优点，但 PHP 没有针对函数式风格进行优化。另一方面，虽然 OOP 是 PHP 的最佳匹配，但所有程序员都可以通过学习其他编程风格（如函数式）来学习有价值的经验。

proach with your hammer, nails, and planks. It's 100 times larger, but you've done this

我建议你阅读 Larry Garfield 写的《Thinking Functionally in PHP》一书。在书中，Larry 清楚地展示了为什么 PHP 不是编写函数式程序的完美语言，但他也用 PHP 解释了 FP 的思维方式。即使你不会编写函数式 PHP 生产代码，我们也可以将很多知识应用到 OOP 中。

before — right? It'll only take a little longer.

我发现一开始很难相信，但类和继承与 Alan 设想的 OOP 方式无关。这并不意味着它们本身是坏事，但思考它们的目的以及我们如何使用（以及滥用）它们是好的。Alan 的愿景只描述了对象——它没有解释这些对象是如何创建的。类后来被添加为管理对象的便捷方式，但它们只是一个实现细节，不是 OOP 的核心思想。随着类的出现，继承也随之而来，这是另一个在正确使用时有用的工具。但情况并不总是如此。

While the scale went up by a factor of 100, its mass went up by a factor of 1,000,000

即使你可能认为它是面向对象设计的支柱之一，它们也经常被滥用，就像 Alan 试图将狗屋扩大到教堂一样。

and its strength only by 10,000. Inevitably, the building will collapse. Some people

OOP 的一个公认优势是它以人类思考世界的方式为我们的代码建模。但实际上，我们很少从抽象和继承的角度思考。我们没有在真正有意义的地方使用继承，而是滥用它来共享代码，并以模糊的方式配置对象。我将向你展示一个很好的例子来说明这个问题，尽管我想提前说明这不是我自己的：它是 Sandi Metz 的，一位关于 OOP 主题的优秀教师。让我们来看看。

plaster over the rubble, make it into a pyramid and say it was the plan all along; but

Sandi 的演讲：https://www.youtube.com/watch?v=OMPfEXIlTVE

you and I know what really went on.

有一个儿童童谣叫"The House That Jack Built"（这也是一部恐怖电影，但与此无关）。它开始是这样的：

You can watch Alan's talk here: https://www.youtube.com/watch?v=oKg1h-

This is the house that Jack built.

TOQXoY

每次迭代，都会添加一个句子：

116

This is the malt that lay in
        the house that Jack built.

Alan used this metaphor to explain a critical problem he saw with "modern OOP" 20

接下来

years ago. I think it still holds today: we've taken the solution to a problem — OO code

This is the rat that ate
        the malt that lay in
        the house that Jack built.

— we've scaled it by a factor of 100, and expected it to work the same way. Even

明白了吗？这是最终的诗：

today, we don't think enough about architecture — which is rather crucial if you're

This is the horse and the hound and the horn that belonged to
        the farmer sowing his corn that kept
        the rooster that crowed in the morn that woke
        the priest all shaven and shorn that married
        the man all tattered and torn that kissed
        the maiden all forlorn that milked
        the cow with the crumpled horn that tossed
        the dog that worried
        the cat that killed
        the rat that ate 
        the malt that lay in
        the house that Jack built.

building a cathedral — we use the OO solutions we learned without any extra thought.

让我们用 PHP 编写这个：一个程序，你可以询问一个给定的迭代，它会生成到那个点的诗。让我们以 OO 的方式来做。我们首先将所有部分添加到一个类中的数据数组中；让我们称那个类为 `PoemGenerator`——听起来很 OO，对吧？很好。

Most of us learned OO in isolation with small examples and rarely at scale. In most

现在让我们添加两个方法 `generate` 和 `phrase`。`generate` 将返回最终结果，`phrase` 是一个将部分粘合在一起的内部函数。

real-life projects, you cannot simply apply the patterns you've learned and expect

看起来我们的解决方案有效：我们可以使用 `phrase` 从数据数组的末尾取出 x 数量的项目，并将它们合并成一个短语。接下来，我们使用 `generate` 将最终结果包装在 `This is` 和 `.` 中。顺便说一下，我在那个空格分隔符上使用 `implode` 只是为了格式化输出更美观。

everything to fall into place the same way it did with Animals, Cats, and Dogs.

正是我们期望的结果。

This reckless scaling of OO code caused many people to voice their disapproval of it

然后来了……一个新的功能请求。让我们构建一个随机诗歌生成器：它将随机化短语的顺序。我们如何在不复制和重复代码的情况下以干净的方式解决这个问题？继承来拯救——对吧？首先，让我们做一个小的重构：让我们添加一个 `protected data` 方法，这样我们在它实际返回的内容上有更多的灵活性：

in recent years. I think that OOP is as good a tool as any other — functional program-

接下来我们构建我们的 `RandomPoemGenerator`：

ming being the modern-day popular contestant — if used correctly.

继承有多棒！我们只需要重写代码的一小部分，一切都能按预期工作！

My takeaway from Alan's talk 20 years ago is that each object is a little program on its

太棒了！

own, with its own internal state. Objects send messages between each other — pack-

再一次……一个新的功能请求：一个回声生成器：它重复每一行第二次。所以你会得到这个：

ages of immutable data — which other objects can interpret and react to. You can't

This is the malt that lay in the malt that lay in
        the house that Jack built the house that Jack built.

write all code this way, and that's acceptable — it's fine to not blindly follow these

我们可以解决这个问题；继承——对吧？

rules. Still, I have experienced the positive impact of this mindset first hand. Thinking

让我们再次在 `PoemGenerator` 中做一个小的重构，只是为了确保我们的代码保持干净。我们可以将 `phrase` 中的数组切片功能提取到它自己的方法中，这似乎是更好的关注点分离。

of objects as little standalone programs, I started writing parts of my code in a differ-

重构后，实现 `EchoPoemGenerator` 再次变得非常容易：

ent style. I hope that, now that we're going to look at object-oriented PHP, you'll keep

我们能否花一点时间欣赏继承的力量？我们已经创建了原始 `PoemGenerator` 的两个不同实现，并且只在 `RandomPoemGenerator` 和 `EchoPoemGenerator` 中重写了与它不同的部分。我们甚至使用了 SOLID 原则（或者我们认为）来确保我们的代码是解耦的，以便很容易重写特定部分。这就是伟大的 OOP 的意义所在——对吧？

Alan's ideas in mind. They taught me to critically look at what I took for granted as

再一次……另一个功能请求：请再做一个实现，一个结合随机和回声行为的实现：`RandomEchoPoemGenerator`。

"proper OO", and learned there's more to it than you might think.

现在怎么办？那个类将扩展哪个？

Alternatives to OOP

如果我们扩展 `PoemGenerator`，我们将不得不重写我们的 `data` 和 `parts` 方法，基本上从 `RandomPoemGenerator` 和 `EchoPoemGenerator` 复制代码。这是糟糕的设计，到处复制代码。如果我们扩展 `RandomPoemGenerator` 呢？我们需要从 `EchoPoemGenerator` 重新实现 `parts`。如果我们实现 `EchoPoemGenerator`，情况会相反。

I don't want to promote any tunnel vision in this book. I'm aware that there are

说实话，扩展 `PoemGenerator` 并复制两个实现似乎是最好的解决方案。因为这样，我们至少向未来的程序员清楚地表明这是一个独立的东西，我们无法用任何其他方式解决它。

other approaches to programming than only OOP. Functional programming, for

但让我们坦率地说：无论什么解决方案，都是垃圾。我们已经陷入了继承的陷阱。亲爱的读者，这在现实项目中经常发生：我们认为继承是重写和重用行为的完美解决方案，它一开始总是看起来很棒。接下来出现了一个新功能，导致更多的抽象，并导致我们的代码失控。我们以为我们掌握了继承，但它却踢了我们的屁股。

example, has seen a tremendous increase in popularity in recent years. While

那么问题是什么——我们代码的实际问题是什么？`RandomPoemGenerator` 从 `PoemGenerator` 扩展不是有道理吗？它是一个诗歌生成器，不是吗？这确实是我们思考继承的方式：使用"是一个"。是的，`RandomPoemGenerator` 是一个 `PoemGenerator`，但 `RandomPoemGenerator` 现在不仅仅是在生成诗歌，不是吗？

I reckon that FP has its merits, PHP isn't optimised to program in a functional

Sandi Metz 建议用以下问题来识别潜在问题："两者之间发生了什么变化——在继承过程中发生了什么变化？"嗯……在 `RandomPoemGenerator` 的情况下，是 `data` 方法；对于 `EchoPoemGenerator`，是 `parts` 方法。碰巧的是，必须结合这两个部分，这就是让我们的继承解决方案爆炸的原因。

style. On the other hand, while OOP is the best match for PHP, all programmers

你知道这意味着什么吗？这意味着 `parts` 和 `data` 是它们自己的东西。它们不仅仅是我们的诗歌生成器的受保护实现细节。它们是客户重视的东西，是我们程序的本质。

Chapter 11 - Object Oriented PHP

所以让我们这样对待它们。

can learn valuable lessons by learning about other programming styles, like a

确定了两个独立的关注点后，我们需要给它们一个合适的名称。第一个是关于行是否应该被随机化。让我们称它为 `Orderer`；它将接收一个原始数组并返回一个新版本，其项目按特定方式排序。

functional one.

第二个关注点是关于格式化输出——是否应该回显。让我们称这个概念为 `Formatter`。它的任务是接收行数组并将所有这些行格式化为一个字符串。

I'd recommend you read a book called "Thinking Functionally in PHP" by Larry

魔法来了。我们从 `PoemGenerator` 中提取这个逻辑，但我们仍然需要一种从内部访问它的方式。所以让我们将 `orderer` 和 `formatter` 注入到 `PoemGenerator` 中：

Garfield. In the book, Larry clearly shows why PHP isn't the perfect language

有了这两个，让我们改变 `phrase` 和 `data` 的实现细节：

to write functional programs with, but he also explains FP's mindset, visualised

最后，让我们实现 `Orderer`：

in PHP. And even though you wouldn't write functional PHP production code,

以及 `Formatter`：

there's lots of knowledge we can apply to OOP as well.

默认实现 `DefaultFormatter` 和 `SequentialOrderer` 可能不会执行任何复杂的操作，但它们仍然是一个有效的业务关注点："顺序排序"和"默认格式"是创建我们以其正常形式所知的诗歌所需的两个有效案例。

The Pitfall of Inheritance

你意识到刚才发生了什么吗？你可能认为我们在编写更多代码，但你忘记了什么……我们可以完全删除我们的 `RandomPoemGenerator` 和 `EchoPoemGenerator`，我们不再需要它们了，我们可以只用 `PoemGenerator` 解决所有情况：

I found it difficult to believe at first, but classes and inheritance have nothing to do

我们可以通过提供适当的默认值让我们的生活更容易一些：

with OOP the way Alan envisioned it. That doesn't mean they are bad things per se,

使用命名属性，我们可以以任何我们想要的方式构造 `PoemGenerator`：

but it is good to think about their purpose and how we can use (as well as abuse)

不再需要第三个抽象！

them. Alan's vision only described objects — it didn't explain how those objects were

这是真正的面向对象编程。我告诉过你 OOP 不是关于继承的，这个例子显示了它的真正力量。通过将对象组合成其他对象，我们能够创建一个灵活且持久的解决方案，一个以干净的方式解决我们所有问题的解决方案。这就是组合优于继承的意义所在，这是 OO 中最基本的支柱之一。

created. Classes were added later as a convenient way to manage objects, but they

我承认：我在开始编写代码时并不总是使用这种方法。在开发过程中，简单地开始而不考虑抽象或组合通常更容易。我甚至会说这是一个很好的规则：不要太早抽象。重要的教训不是你总是应该使用组合。相反，它是关于识别你遇到的问题并使用正确的解决方案来解决它。

are only an implementation detail, not OOP's core idea. With classes came inheritance,

你可能在想使用 traits 来解决我们的诗歌问题。你可以创建一个 `RandomPoemTrait` 和 `EchoPoemTrait`，实现 `data` 和 `phrase`。是的，traits 可以是另一个解决方案，就像继承也是一个可行的解决方案一样。我将说明为什么组合仍然是更好的选择，但首先让我们在实践中展示这些 traits 会是什么样子：

another useful tool when used correctly. That hasn't always been the case, though.

你可以这样使用这些来实现 `RandomEchoPoemGenerator`：

Even when you might think it's one of the pillars of object-oriented design, they are

Traits 确实解决了代码可重用性问题；这正是它们被添加到语言中的原因。当我提到添加 `RandomEchoPoemGenerator` 的最新功能请求时，我评论说没有干净的方法来解决这个问题而不复制代码，这是寻找另一个解决方案——组合——的垫脚石。我是否故意忽略 traits 来证明我的观点？不。虽然它们确实解决了可重用性问题，但它们没有我们在探索组合时发现的额外好处。

misused very often, just like the doghouse Alan tried to scale up to a cathedral.

首先，我们发现诗歌的顺序和格式是关键的业务规则，不应该被视为类中某处的受保护实现细节。我们创建了 `Orderer` 和 `Formatter` 来使我们的代码更好地代表我们试图解决的现实世界问题。如果我们选择 traits 和子类，我们再次失去这种明确性。

One of OOP's acclaimed strengths is that it models our code in ways humans think

其次，我们的诗歌示例显示了 `PoemGenerator` 的两个可配置部分。如果有三个或四个呢？如果我们添加两个更多的 traits，我们还必须为这些 traits 创建新的子类实现，以及与现有 traits 的所有相关组合。子类的数量会呈指数级增长。即使在我们当前的示例中，已经有三个子类：`RandomPoemGenerator`、`EchoPoemGenerator` 和 `RandomEchoPoemGenerator`。另一方面，组合只需要我们添加两个新类。如果有更复杂的业务规则需要考虑，我们的代码会失控。

about the world. In reality, though, we rarely think in terms of abstractions and inher-

我并不是建议根本不应该使用 traits；就像继承一样，它们有它们的用途。最重要的是，你要批判性地评估所有解决方案的优缺点，而不是退回到最初看起来最容易的解决方案。

itance. Instead of using inheritance in places where it actually makes sense, we've

我认为这种推理适用于所有与编程相关的事情，无论你是在面向对象、过程式还是函数式风格中编码。OOP 得到了一个坏名声，因为人们开始不加思考地扩展它，而没有重新思考他们的架构。我希望我们能改变这一点。

been abusing it to share code, and configure objects in an obscure way. I'm going to

show you a great example that illustrates this problem, though I want to say upfront

that it isn't my own: it's Sandi Metz's, a great teacher on the subject of OOP. Let's take

a look.

Sandi's talk: https://www.youtube.com/watch?v=OMPfEXIlTVE

118

There's a children's nursery rhyme called "The House That Jack Built" (it's also a

horror movie, but that's unrelated). It starts like this:

This is the house that Jack built.

Every iteration, there's a sentence added to it:

This is the malt that lay in

the house that Jack built.

And next

This is the rat that ate

the malt that lay in

the house that Jack built.

Chapter 11 - Object Oriented PHP

Get it? This is the final poem:

This is the horse and the hound and the horn that belonged to

the farmer sowing his corn that kept

the rooster that crowed in the morn that woke

the priest all shaven and shorn that married

the man all tattered and torn that kissed

the maiden all forlorn that milked

the cow with the crumpled horn that tossed

the dog that worried

the cat that killed

the rat that ate

the malt that lay in

the house that Jack built.

Let's code this in PHP: a program that you can ask a given iteration, and it will produce

the poem up until that point. Let's do it in an OO way. We start by adding all parts

into a data array within a class; let's call that class PoemGenerator — sounds very OO,

right? Good.

class PoemGenerator

{

private static array $data = [

'the horse and the hound and the horn that belonged to',

'the farmer sowing his corn that kept',

'the rooster that crowed in the morn that woke',

'the priest all shaven and shorn that married',

'the man all tattered and torn that kissed',

'the maiden all forlorn that milked',

'the cow with the crumpled horn that tossed',

'the dog that worried',

120

'the cat that killed',

'the rat that ate',

'the malt that lay in',

'the house that Jack built',

];

}

Now let's add two methods generate and phrase. generate will return the end result,

and phrase is an internal function that glues the parts together.

class PoemGenerator

{

// …

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

It seems like our solution works: we can use phrase to take x-amount of items from

the end of our data array and implode those into one phrase. Next, we use generate

Chapter 11 - Object Oriented PHP

to wrap the final result with This is and .. By the way, I implode on that spaced de-

limiter just to format the output a little nicer.

$generator = new PoemGenerator();

$generator=>generate(4);

// This is the cat that killed

//         the rat that ate

//         the malt that lay in

//         the house that Jack built.

Exactly what we'd expect the result to be.

Then comes along… a new feature request. Let's build a random poem generator: it

will randomise the order of the phrases. How do we solve this in a clean way without

copying and duplicating code? Inheritance to the rescue — right? First, let's do a little

122

refactor: let's add a protected data method so that we have a little more flexibility in

what it actually returns:

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

'the horse and the hound and the horn that belonged to',

// …

'the house that Jack built',

];

}

}

Chapter 11 - Object Oriented PHP

Next we build our RandomPoemGenerator:

class RandomPoemGenerator extends PoemGenerator

{

protected function data(): array

{

$data = parent=:data();

shuffle($data);

return $data;

}

}

How great is inheritance! We only needed to override a small part of our code, and

everything works just as expected!

$generator = new RandomPoemGenerator();

$generator=>generate(4);

// This is the priest all shaven and shorn that married

//         the cow with the crumpled horn that tossed

//         the man all tattered and torn that kissed

//         the rooster that crowed in the morn that woke.

Awesome!

124

Once again… a new feature request: an echo generator: it repeats every line a second

time. So you'd get this:

This is the malt that lay in the malt that lay in

the house that Jack built the house that Jack built.

We can solve this; inheritance — right?

Let's again do a small refactor in PoemGenerator, just to make sure our code stays

clean. We can extract the array slicing functionality in phrase to its own method, which

seems like a better separation of concerns.

class PoemGenerator

{

// …

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

Chapter 11 - Object Oriented PHP

Having refactored this, implementing EchoPoemGenerator is again very easy:

class EchoPoemGenerator extends PoemGenerator

{

protected function parts(int $number): array

{

return array_reduce(

parent=:parts($number),

fn (array $output, string $line) =>

[==.$output, "{$line} {$line}"],

[]

);

}

}

Can we take a moment to appreciate the power of inheritance? We've created two

different implementations of our original PoemGenerator, and have only overridden the

parts that differ from it in RandomPoemGenerator and EchoPoemGenerator. We've even

used SOLID principles (or so we think) to ensure that our code is decoupled so that

it's easy to override specific parts. This is what great OOP is about — right?

One more time… another feature request: please make one more implementation, one

that combines both the random and echo behaviour: RandomEchoPoemGenerator.

Now what? Which class will that one extend?

If we're extending PoemGenerator, we'll have to override both our data and

parts methods, essentially copying code from both RandomPoemGenerator and

126

EchoPoemGenerator. That's bad design, copying code around. What if we extend

RandomPoemGenerator? We'd need to reimplement parts from EchoPoemGenerator. If

we'd implement EchoPoemGenerator instead, it would be the other way around.

To be honest, extending PoemGenerator and copying both implementations seems like

the best solution. Since then, we're at least making it clear to future programmers that

this is a thing on its own, and we weren't able to solve it any other way.

But let's be frank: whatever solution, it's all crap. We have fallen into the pitfall that

is inheritance. And this, dear reader, happens so often in real-life projects: we think

of inheritance as the perfect solution to override and reuse behaviour, and it always

seems to work great at the start. Next comes along a new feature that causes more

abstractions, and causes our code to grow out of hand. We thought we mastered

inheritance but it kicked our asses instead.

So what's the problem — the actual problem — with our code? Doesn't it make

sense that RandomPoemGenerator extends from PoemGenerator? It is a poem gen-

erator, isn't it? That's indeed the way we think of inheritance: using "is a". And yes,

RandomPoemGenerator is a PoemGenerator, but RandomPoemGenerator isn't only gener-

ating a poem now, is it?

Sandi Metz suggests the following question to identify the underlying problem: "what

changed between the two — what changed during inheritance?". Well… In the case

of RandomPoemGenerator, it's the data method; for EchoPoemGenerator, it's the parts

method. And it just so happens that having to combine those two parts is what made

our inheritance solution blow up.

Do you know what this means? It means that parts and data are something on their

own. They are more than a protected implementation detail of our poem generator.

They are what is valued by the client, they are the essence of our program.

So let's treat them as such.

Chapter 11 - Object Oriented PHP

With two separate concerns identified, we need to give them a proper name. The first

one is about whether lines should be randomised or not. Let's call it the Orderer; it will

take an original array and return a new version of it with its items sorted in a specific

way.

interface Orderer

{

public function order(array $data): array;

}

The second concern is about formatting the output - whether it should be echoed

or not. Let's call this concept a Formatter. Its task is to receive the array of lines and

format all of those lines into one string.

interface Formatter

{

public function format(array $lines): string;

}

128

And here comes the magic. We're extracting this logic from our PoemGenerator, but we

still need a way to access it from within. So let's inject both an orderer and formatter

into the PoemGenerator:

class PoemGenerator

{

public function =_construct(

public Formatter $formatter,

public Orderer $orderer,

) {}

// …

}

Chapter 11 - Object Oriented PHP

With both available, let's change the implementation details of phrase and data:

class PoemGenerator

{

// …

protected function phrase(int $number): string

{

$parts = $this=>parts($number);

return $this=>formatter=>format($parts);

}

protected function data(): array

{

return $this=>orderer=>order([

'the horse and the hound and the horn that belonged to',

// …

'the house that Jack built',

]);

}

}

130

And finally, let's implement Orderer:

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

Chapter 11 - Object Oriented PHP

As well as Formatter:

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

fn (array $output, string $line) =>

[==.$output, "{$line} {$line}"],

[]

);

return implode("\n        ", $lines);

}

}

The default implementations, DefaultFormatter and SequentialOrderer might not

do any complex operations, though still they are a valid business concern: a "sequen-

tial order" and "default format" are two valid cases needed to create the poem as we

know it in its normal form.

Do you realise what just happened? You might be thinking that we're writing more

code, but you're forgetting something… we can remove our RandomPoemGenerator and

132

EchoPoemGenerator altogether, we don't need them anymore, we can solve all of our

cases, with only the PoemGenerator:

$generator = new PoemGenerator(

new EchoFormatter(),

new RandomOrderer(),

);

We can make our lives still a little easier by providing proper defaults:

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

Chapter 11 - Object Oriented PHP

And using named properties, we can construct a PoemGenerator whatever way we

want:

$generator = new PoemGenerator(

formatter: new EchoFormatter(),

);

$generator = new PoemGenerator(

orderer: new RandomOrderer(),

);

$generator = new PoemGenerator(

formatter: new EchoFormatter(),

orderer: new RandomOrderer(),

);

No more need for a third abstraction!

This is real object-oriented programming. I told you that OOP isn't about inheritance,

and this example shows its true power. By composing objects out of other objects,

we're able to make a flexible and durable solution, one that solves all of our problems

in a clean way. This is what composition over inheritance is about, and it's one of the

most fundamental pillars in OO.

I'll admit: I don't always use this approach when I start writing code. It's often easier to

start simply during the development process and not think about abstracts or com-

position. I'd even say it's a great rule to follow: don't abstract too soon. The important

134

lesson isn't that you should always use composition. Instead, it's about identifying the

problem you encounter and using the right solution to solve it.

What about traits?

You might be thinking about traits to solve our poem problem. You could make a

RandomPoemTrait and EchoPoemTrait, implementing data and phrase. Yes, traits can

be another solution, just like inheritance also is a working solution. I'm going to make

the case why composition is still the better choice, but first let's show in practice what

these traits would look like:

trait RandomPoemTrait

{

protected function data(): array

{

$data = parent=:data();

shuffle($data);

return $data;

}

}

Chapter 11 - Object Oriented PHP

trait EchoPoemTrait

{

protected function parts(int $number): array

{

return array_reduce(

parent=:parts($number),

fn (array $output, string $line) =>

[==.$output, "{$line} {$line}"],

[]

);

}

}

You could use these to implement RandomEchoPoemGenerator like so:

class RandomEchoPoemGenerator extends PoemGenerator

{

use RandomPoemTrait;

use EchoPoemTrait;

}

Traits indeed solve the problem of code reusability; that's exactly why they

were added to the language. When I mentioned the latest feature request to add

RandomEchoPoemGenerator, I remarked that there was no clean way to solve the

problem without code duplication, which was the stepping stone to search for another

solution — composition. Did I deliberately ignore traits to make my point? No. While

they do solve the problem of reusability, they don't have the added benefits we dis-

covered when exploring composition.

First we discovered that the order and format of the poem are crucial business rules

and shouldn't be treated as protected implementation details somewhere in the class.

136

We made Orderer and Formatter to make our code better represent the real-world

problem we're trying to solve. If we're choosing traits and subclasses instead, we lose

this explicitness once again.

Second, our poem example shows two parts of the PoemGenerator that are config-

urable. What if there's three or four? If we're adding two more traits, we also have

to create new subclass implementations for those traits, and all relevant combina-

tions with existing traits. The number of subclasses would grow exponentially. Even

with our current example, there's already three subclasses: RandomPoemGenerator,

EchoPoemGenerator and RandomEchoPoemGenerator. Composition on the other hand

only requires us to add only two new classes. Our code would grow out of hand if

there were more complex business rules to account for.

I'm not suggesting traits shouldn't be used at all; just like inheritance, they have their

uses. What's most important is that you critically assess the pros and cons of all solu-

tions for a given problem instead of falling back to what seems the easiest at first.

I think this reasoning applies to everything programming related, whether you're

coding in an object-oriented, procedural, or functional style. OOP got a bad name

because people started to scale it out of hand, without rethinking their architecture. I

hope we can change that.

