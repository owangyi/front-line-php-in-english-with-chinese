# Chapter 23: Event Driven

CHAPTER 23

事件溯源、CQRS、事件驱动；这些神秘的术语如果你从未在事件驱动系统中工作过，可能会令人生畏。即使你有，也有很多意见、理论和模式。总的来说，它可能看起来是一个非常复杂的问题。

Event Driven Development

事件驱动系统不是所有问题的解决方案。虽然它们增加了一层灵活性，但它们也消除了简单性和明确性。

Event sourcing, CQRS, event-driven; these mystical terms can seem daunting if you've

在其核心，事件驱动开发并不那么困难。是建立在简单概念之上的模式使其更加困难，但也更强大。这种力量在复杂和大型应用程序中经常需要，确实：PHP 经常用于构建这样的应用程序。我想专门用一章来讨论这个话题，因为你可能必须在你的事业中处理某种形式的事件驱动系统。有一些背景信息很重要。

never worked in an event-driven system before. And even if you have, there are lots of

所以让我们从基础开始。

opinions, theories, and patterns. It still might seem like a very complex matter overall.

事件驱动系统的想法是，你远离微观管理程序流程，而是允许单个组件在发生某些事情时做出反应。一个例子：与其有一个管理"发票创建"的单个函数或服务，可以有多个小服务，每个处理发票创建过程的一部分。起点是发票被创建；接下来有一个生成 PDF 并将其保存在文件系统上的服务；还有一个向客户发送电子邮件通知他们有关待处理发票的服务。

Event-driven systems aren't the solution to all problems. While they add a layer of

我在一个段落中使用了三个术语来描述"在发生某些事情时做出反应的代码片段"。你甚至可能想称它们为"微服务"。现在，我们不会专注于这些服务如何相互通信的技术细节，并假设它们实际上是同一代码库中的简单对象，在同一服务器上运行；从这里开始，我将它们称为普通的"服务"。

flexibility, they also remove simplicity and explicitness.

顺便说一下，你注意到 Alan Kay 对"对象"是什么的愿景如何完美地适合这个模型吗？我喜欢当事情结合在一起时！

At its core, event-driven development isn't all that difficult. It's the patterns that build

这些服务不一定需要相互了解：每当系统中发生某些事情时，它们就会做出反应。这个"某事"被称为"事件"。

upon a simple concept that make it more difficult, but also more powerful. This power

从技术角度来看，事件驱动系统需要的只是一个事件总线：它是知道所有监听事件的服务的中心位置；我们也可以称它们为"事件订阅者"。每当事件发生时，事件总线会被通知，这反过来会通知所有相关的订阅者。自己编写一个简单的事件总线并不困难。例如，这里是一个只有几行代码的实现：

is often needed in complex and large applications, and indeed: PHP is often used to

你可以想出很多细节和补充，但在其核心，这就是你需要的全部：一个可以在事件被分派时通知的订阅者列表。

build such applications. I wanted to dedicate a chapter on the topic since you'll proba-

没有什么阻止你使这样的事件总线异步。事实上，事件驱动系统在进行异步编程时经常被首选：它是一个非常适合并行和异步思维的模型。

bly have to deal with some form of event-driven systems in your career. It's important

对于我们的例子，我们假设事件总线总是同步处理事件：这样更容易推理事件流程，并消除我们否则必须处理的许多技术细节。

to have some background information.

在我们的发票例子中，我们有两个订阅 `InvoiceCreatedEvent` 事件的服务：

So let's start with the basics.

不过，我们的实现可以进行一些改进。通过为事件总线添加一些反射功能，我们可以根据方法签名确定订阅者是否应该处理事件。这不仅使我们的代码更加简洁，还允许我们在订阅者中确切知道我们正在处理什么类型的事件。让我们想象我们已经重构了事件总线，现在可以这样编写订阅者：

The idea of an event-driven system is that you step away from micro-managing the

让我们继续深入探索我们的事件驱动系统。它有一个大的注意事项——事实上，它是所有事件驱动系统的主要特征：间接性。

program flow and instead allow individual components to react whenever something

想象发票创建，`InvoiceCreatedEvent` 在发票创建后被触发：

happens. An example: instead of having a single function or service that manages

虽然事件驱动开发承诺灵活性——你可以连接任意数量的订阅者——但它也导致了一种间接耦合。我们不知道当我们触发这个事件时会发生什么；我们需要相信正确的订阅者会在我们看不到的情况下处理它。这种间接层可能使调试程序流程变得更加困难，即使事件是同步处理的。

the "creation of an invoice", there can be several small services, each handling a part

除此之外：分派事件后，你不能有任何直接返回值，因为无限数量的订阅者可以处理该事件。不过，你可以引入一些轮询层来观察结果，例如，在数据库中。尽管如此，你必须处理许多复杂性：以简单性为代价的灵活性。

of the invoice creation process. The starting point is the invoice being created; next

你注意到我们还没有编写任何"事件溯源"或"CQRS"代码，但我们已经在使用事件驱动程序了吗？你不需要事件溯源、命令总线、CQRS 或最简单形式的微服务。你只需要事件。

there's a service that generates a PDF and saves it on the filesystem; and one that

不过，如果有足够的时间，任何在这样的事件驱动系统中工作的开发者都会遇到这种简化方法的问题。

sends an email to the customer notifying them about a pending invoice.

可能有广泛的性能问题：降级的开发者体验、扩展问题或管理一致性和状态的问题。你会自然地尝试通过应用模式和原则来解决这些问题，这正是事件驱动社区多年来一直在做的事情。他们提出了模式来帮助解决更困难的问题，你在现实、复杂系统中会遇到的问题。

236

Martin Fowler 编写并谈论了几种这样的模式，以及社区如何发现它们。在本章的下半部分，我将简要讨论其中四种模式，所有这些都经常被使用。相关链接列在本章末尾。

Service? Object? Function?

事件驱动系统的最简单形式称为"事件通知"：事件仅用于通知发生了某些事情。我们使用 `InvoiceCreatedEvent` 的例子已经比这更复杂，因为我们使用请求数据并将其与事件一起发送。

I've used three terms in one paragraph to describe "a piece of code that reacts

使用事件通知，事件只表示发生了某些事情。服务本身负责访问数据库、第三方服务或外部状态，并确定它们想要使用的数据。这也是事件驱动开发的最弱形式：一切都仍然耦合在一起。唯一的区别是你使用事件的灵活性将一个事件连接到多个服务。

when something happens". You might even think about calling them "micro

第二个模式是我们在例子中应用的：我们在事件发生时捕获了相关数据，并将其与事件一起发送。处理该事件的所有服务只允许使用由该事件封装的数据。

services". For now, we won't focus on the technicalities of how these services

这种方法确保我们可以有多个服务监听同一事件，而不必担心它们被处理的顺序。我们总是确定我们的服务不会依赖外部状态，所以事件成为"真理的来源"。

communicate with each other and assume they are, in fact, simple objects in the

建立在事件携带所有必要状态的想法之上的是事件溯源。与其保存，例如，发票到数据库，如果我们保存事件本身会发生什么？那会有益吗？

same codebase, running on the same server; I'll call them plain old "services"

如果事件成为真理的来源并保存到数据库，我们总是有一层额外的信息可用。与其知道最终结果的样子（发票），我们现在也知道构成该结果的步骤（事件）。

from here on out.

看看这个事件列表，也称为"事件流"：

By the way, have you noticed how Alan Kay's vision of what "objects" are per-

如果我们只使用事件来触发服务做某事，我们会在事件被处理后丢失事件的数据。传统应用程序经常处理这类问题，这就是为什么它们在数据库中跟踪状态变化：像 `created_at` 或 `payment_date` 这样的列被添加到发票上，必须从那里仔细管理。

fectly fits this model? I like it when things come together!

不过，如果我们直接保存事件，我们可以从存储（数据库、文件系统或其他东西）中检索它们，并从头动态重建我们的应用程序状态。例如，我们可以重建这些事件的结果发票——至少只要那些存储的事件携带所有相关数据。

These services don't necessarily need to know about each other: they react whenever

这就是事件溯源的力量：能够仅使用事件重建整个应用程序状态。它为有趣的用例打开了大门。例如，我们可以开始基于这些事件中可用的历史数据生成报告。我们可以生成一个报告，分析客户在发票发送给他们后支付发票所需的平均时间，而无需重写我们的数据模型。没错：我们需要的所有数据已经存储为事件，我们只需要以新的方式解释它们。

something happens in the system. This "something" is called an "event".

不过，事件溯源带来了许多其他问题。最紧迫的一个：性能。生产应用程序会随着时间的推移存储数百万个事件；当然，我们不能在每次请求到来时从头重建整个应用程序状态。这就是为什么有其他模式帮助我们解决这类问题：投影和快照经常用于构建缓存和可重用的状态，而不是总是从头重建它。一个实际的例子可能是发票投影：一个存储所有这些发票事件的最终结果的表，我们可以轻松地从中读取数据。

From a technical point of view, all an event-driven system needs is an event bus: it's

经常与事件溯源一起出现的另一个抽象是进行更改的意图和更改本身之间的区别。当我们直接触发 `InvoiceCreatedEvent` 时，感觉有点不对：发票本身还没有被创建。相反，将意图称为 `CreateInvoice` 并将实际结果存储在数据库中的 `InvoiceCreated` 会更有意义。第一个通常被称为"命令"，而第二个被称为"事件"。

the central place that knows about all services listening for events; we could also

当我们试图正确应用事件溯源时，会出现很多复杂性。那是因为与我们最基本的实现也增加复杂性的相同原因：这是我们为更灵活和可扩展的系统付出的代价。记住这一点：事件驱动架构并不总是问题的正确解决方案。很可能一个更简单的方法不仅更快，而且更好。

call them "event subscribers". Whenever an event happens, the event bus is notified,

一位明智的开发者 Frank De Jonge 曾经说过："事件溯源使简单的问题变难，使困难的问题变简单"。在将事件溯源添加到项目之前，确保你已经权衡了利弊。

which in turn will notify all relevant subscribers. It's not difficult at all to program a

CQRS——命令查询责任分离——是我想涉及的第四个也是最后一个模式。Martin Fowler 这样描述它："其核心概念是，你可以使用不同的模型来更新信息，而不是用于读取信息的模型。对于某些情况，这种分离可能很有价值[…]理由是对于许多问题，特别是在更复杂的领域，为命令和查询使用相同的概念模型会导致一个更复杂的模型，两者都做不好。"

simple event bus yourself. For example, here's an implementation in only a few lines of

换句话说：CQRS 旨在分离写入数据和读取数据的关注点。它再次允许更多的灵活性。请记住，这是一个用于非常复杂系统的模式。Martin Fowler 甚至警告不要过快使用 CQRS："尽管有这些好处，你应该非常谨慎地使用 CQRS。许多信息系统非常适合信息库的概念，它以与读取相同的方式更新，将 CQRS 添加到这样的系统可能会增加显著的复杂性。"

code:

关于事件驱动系统还有更多要说的，但这超出了本书的范围。有几个 PHP 框架促进了事件驱动系统，但最重要的是事件驱动思维，而不是一堆技术工具。我希望你对这种思维由什么有了一点了解，如果你对它感兴趣，我建议查看一些关于这个话题的更多资源。

interface Subscriber

Martin Fowler 对事件驱动架构的介绍：https://www.youtube.com/watch?v=STKCRSUsyP0

{

Greg Young 分享关于 DDD、CQRS 和事件溯源的见解：https://www.youtube.com/watch?v=LDW0QWie21s

public function handles(object $event): bool;

我承认完成这本书对我来说是一个有点情感的时刻。我已经在这个项目上工作了四年多；首先在我的博客上单独工作，然后与我在 Spatie 的出色同事一起工作。

public function handle(object $event): void;

我觉得我说了我想说的话。尽管关于 PHP 开发还有很多要教的内容，但这本书已经奠定了坚实的基础。感觉所有那些在我脑海中漂浮的独立话题终于在一个地方连接起来了。

}

我希望你的学习过程不会随着这本书而停止。即使合适的学习材料很难获得，我鼓励你继续挑战自己，作为专业开发者成长。这就是我多年来一直在做的事情：不断学习和不断成长。

Chapter 23 - Event Driven Development

所以最后，感谢阅读，我真的希望我能够在你永无止境的学习和成长过程中帮助你。

class EventBus

谢谢，  
Brent

{

PS：如果你想要一个所有新的和花哨的 PHP 语法的快速摘要，你可以访问 https://front-line-php.com/cheat-sheet 并浏览我们方便的小抄。

private array $subscribers = [];

public function addSubscriber(Subscriber $subscriber): self

{

$this=>subscribers[] = $subscriber;

}

public function dispatch(object $event): void

{

foreach ($this=>subscribers as $subscriber) {

if (! $subscriber=>handles($event)) {

continue;

}

$subscriber=>handle($event);

}

}

}

You can come up with lots of niceties and additions, but at its very core, this is all you

need: a list of subscribers that can be notified whenever an event is dispatched.

Asynchronous

Nothing is stopping you from making such an event bus asynchronous. In fact,

an event-driven system is often preferred when doing async programming: it's a

model that fits the parallel and async mindset extremely well.

238

For our examples, we'll assume the event bus always processes events syn-

chronously: it's much simpler to reason about the event flow that way and elimi-

nate many technicalities we'd have to deal with otherwise.

In our invoice example, we'd have two services that subscribe to the

InvoiceCreatedEvent event:

class InvoicePdfService implements Subscriber

{

public function handles(object $event): bool

{

return $event instanceof InvoiceCreatedEvent;

}

public function handle(object $event): void

{

// Generate invoice PDF and save it on the filesystem

}

}

class InvoiceMailService implements Subscriber

{

public function handles(object $event): bool

{

return $event instanceof InvoiceCreatedEvent;

}

Chapter 23 - Event Driven Development

public function handle(object $event): void

{

// Send mail with a link to the customer's invoice page

}

}

Our implementation could do with a little polishing, though. By adding some reflection

capabilities to our event bus, we can determine whether a subscriber should handle

an event based on its method signature instead. This not only makes our code more

concise, but also allows us to know exactly what kind of event we're dealing with in

our subscribers. Let's imagine we've refactored our event bus, and can now write

subscribers like so:

class InvoicePdfService

{

public function handle(InvoiceCreatedEvent $event): void

{

// Generate invoice PDF and save it on the filesystem

}

}

Let's continue exploring our event-driven system in depth. There's one big caveat

with it - in fact, it's the major characteristic of all event-driven systems: indirectness.

240

Imagine the invoice creation the InvoiceCreatedEvent being triggered after the

invoice was created:

public function createInvoice()

{

$invoice = /* … */;

$event = new InvoiceCreatedEvent($invoice);

$this=>eventBus=>dispatch($event);

}

While event-driven development promises flexibility — you can hook up as many sub-

scribers as you want — it also causes a form on indirect coupling. We don't know what

exactly will happen when we're triggering this event; we need to trust that the right

subscribers will handle it without us seeing. This layer of indirectness can make de-

bugging the program flow much harder, even when events are handled synchronously.

On top of that: you can't have any direct return value after dispatching an event, since

an infinite amount of subscribers can handle that event. However, you could introduce

some polling layer to observe the results in, for example, a database. Still, there are

many complications you have to deal with: flexibility at the cost of simplicity.

Did you notice that we haven't written any "event sourcing" or "CQRS" code, yet still,

we're already working with an event-driven program?. You don't need event sourcing,

a command bus, CQRS, or micro services in its simplest form. You only need events.

Given enough time, though, any developer working in such an event-driven system

would encounter problems with this simplified approach.

There could be a wide range of performance issues: degraded developer experience,

scaling issues, or problems with managing consistency and state. You would natural-

ly try to solve those problems by applying patterns and principles, and that's exactly

what the event-driven community has been doing for years now. They have come up

Chapter 23 - Event Driven Development

with patterns to help tackle the more difficult problems, the ones you'd encounter in

real-life, complex systems.

Martin Fowler writes and talks about several such patterns, and how the community

discovered them. In the next part of this chapter, I will briefly discuss four of those

patterns, all of which are often used. The relevant links are listed at the end of this

chapter.

Event Notification

The simplest form of an event-driven system called "Event Notification": events are

merely used to notify about something that has happened. Our example with the

InvoiceCreatedEvent is already more complex than this since we're using the request

data and sending it along with the event.

With event notifications, the event only signifies that something happened. It's up to

the services themselves to reach out to the database, a third-party service, or outer

state and determine what data they want to use. This is also the weakest form of

event-driven development: everything is still coupled together. The only difference is

that you're using the flexibility of events to hook several services up to one event.

Event-Carried State Transfer

The second pattern is what we have applied in our example: we've captured the

relevant data when the event occurred and sent it together with the event. All ser-

vices handling that event are only allowed to use the data that's encapsulated by that

event.

242

This approach ensures that we can have multiple services listening to the same event

and don't have to worry about which order they are handled in. We're always sure our

services won't rely on the external state, so the event becomes "a source of truth".

Event Sourcing

Built upon the idea of events carrying all necessary state comes event sourcing.

Instead of saving, for example, an invoice to the database, what would happen if we'd

save the events themselves? Would that be beneficial?

If events become the source of truth and are saved to the database, there's a layer

of extra information available to us at all times. Instead of knowing how the end result

looks (the invoice), we now also know what the steps were that constituted that result

(the events).

Take a look at this list of events, also called an "event stream":

[

InvoiceDraftCreated=:class,

InvoiceSent=:class,

InvoicePaid=:class,

]

If we used events only to trigger a service to do something, we'd lose the event's

data after it was handled. Traditional applications often deal with these kinds of

problems, which is why they keep track of state changes in the database: columns

like created_at or payment_date are added on the invoice and have to be carefully

managed from there on out.

Chapter 23 - Event Driven Development

If we're saving the events directly, though, we can retrieve them from a store (a

database, filesystem, or something else), and rebuild our application state dynami-

cally from scratch. For example, we can rebuild the invoice that would be the result of

these events - at least as long as those stored events carry all the relevant data with

them.

That's the power of event sourcing: being able to rebuild the whole application state,

only by using events. It opens doors for interesting use cases. We could, for example,

start generating reports based on the historical data that's available within these

events. We could generate a report that analyses the average time it takes for cus-

tomers to pay their invoice after it was sent to them, without rewriting our data model.

That's right: all the data we need is already stored as events, we just need to interpret

them in a new way.

With event sourcing come lots of other problems, though. The most pressing one:

performance. A production application will store millions upon millions of events over

time; surely, we can't rebuild our whole application state from scratch every time a

request comes in. That's why there are other patterns helping us with those kinds of

problems: projections and snapshots are often used to build a cached and reusable

state, instead of always rebuilding it from scratch. A practical example could be an

invoice projection: a table that stores the end result of all those invoice events and

where we can easily read data from.

Another abstraction that often comes with event sourcing is the difference between

the intention of making a change, and the change itself. When we directly triggered an

InvoiceCreatedEvent, it felt a little off: the invoice itself wasn't created yet. Instead it

would make more sense to have the intent called CreateInvoice and the actual result

to store in the database InvoiceCreated. The first one is often called the "command",

while the second one is called the "event".

A lot of complexity appears when we're trying to apply event sourcing properly. That's

because of the same reasons our most basic implementation also added complexi-

ty: it's the cost we pay for a more flexible and scalable system. Keep this in mind: an

244

event-driven architecture isn't always the right solution for a problem. It might very

well be that a simpler approach is not only faster but also better.

A wise developer, Frank De Jonge, once said: "Event Sourcing makes simple problems

hard, and hard problems simple". Make sure you've weighed the pros and cons before

adding event sourcing to your project.

CQRS

CQRS — command query responsibility segregation — is the fourth and final pattern

I want to touch on. Martin Fowler describes it like this: "At its heart is the notion that

you can use a different model to update information than the model you use to read

information. For some situations, this separation can be valuable […] The rationale is

that for many problems, particularly in more complicated domains, having the same

conceptual model for commands and queries leads to a more complex model that

does neither well."

In other words: CQRS aims to separate the concerns of writing data and reading data.

It again allows for more flexibility. Keep in mind that it's a pattern for very complex

systems. Martin Fowler even warns not to use CQRS too quickly: "Despite these bene-

fits, you should be very cautious about using CQRS. Many information systems fit well

with the notion of an information base that is updated in the same way that it's read,

adding CQRS to such a system can add significant complexity."

There's lots more to tell about event-driven systems, but it's outside the scope of this

book. Several PHP frameworks facilitate an event-driven system, but most important

is the event-driven mindset instead of a bunch of technical tools. I hope you've got a

bit of an idea of what that mindset consists of, and I recommend checking out some

more resources on the topic if you're interested in it.

Chapter 23 - Event Driven Development

Some More Resources

Martin Fowler's introduction to event-driven architecture: https://www.youtube.

com/watch?v=STKCRSUsyP0

Greg Young sharing insights on DDD, CQRS and Event Sourcing: https://www.

youtube.com/watch?v=LDW0QWie21s

246

In Closing

I admit that finishing this book is somewhat of an emotional moment for me. I've been

working on this project for over four years now; first individually on my blog, then to-

gether with my awesome colleagues at Spatie.

I feel that I said what I had to say. Even though there's much more to teach about PHP

development, this book has laid a strong foundation. It feels like all those separate

topics floating around my head finally got connected in one place.

My hope is that your learning process doesn't stop with this book. Even though proper

learning material is hard to come by, I encourage you to keep challenging yourselves

to grow as professional developers. That's what I've been doing for years now: keep

learning and keep growing.

So in closing, thanks for reading, and I truly hope I was able to help you in your never-

ending process of learning and growing.

Thanks,

Brent

PS: If you want a quick summary of all the new and fancy PHP syntax, you can head

over to https://front-line-php.com/cheat-sheet and browse our handy cheat-sheet.

