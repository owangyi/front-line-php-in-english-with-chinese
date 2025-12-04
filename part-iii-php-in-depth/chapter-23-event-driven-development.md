# CHAPTER 23

## EVENT DRIVEN DEVELOPMENT Event Driven Development

Event sourcing, CQRS, event-driven; these mystical terms can seem daunting if you've never worked in an event-driven system before. And even if you have, there are lots of opinions, theories, and patterns. It still might seem like a very complex matter overall. 

Event-driven systems aren't the solution to all problems. While they add a layer of flexibility, they also remove simplicity and explicitness.

At its core, event-driven development isn't all that difficult. It's the patterns that build upon a simple concept that make it more difficult, but also more powerful. This power is often needed in complex and large applications, and indeed: PHP is often used to build such applications. I wanted to dedicate a chapter on the topic since you'll proba -

bly have to deal with some form of event-driven systems in your career. It's important to have some background information.

So let's start with the basics.

The idea of an event-driven system is that you step away from micro-managing the program flow and instead allow individual components to react whenever something happens. An example: instead of having a single function or service that manages the "creation of an invoice", there can be several small services, each handling a part of the invoice creation process. The starting point is the invoice being created; next there's a service that generates a PDF and saves it on the filesystem; and one that sends an email to the customer notifying them about a pending invoice.Service? Object? Function?

I've used three terms in one paragraph to describe "a piece of code that reacts when something happens". You might even think about calling them "micro services". For now, we won't focus on the technicalities of how these services communicate with each other and assume they are, in fact, simple objects in the same codebase, running on the same server; I'll call them plain old "services" 

from here on out.

By the way, have you noticed how Alan Kay's vision of what "objects" are per -

fectly fits this model? I like it when things come together!

These services don't necessarily need to know about each other: they react whenever something happens in the system. This "something" is called an "event".

From a technical point of view, all an event-driven system needs is an event bus: it's the central place that knows about all services listening for events; we could also call them "event subscribers". Whenever an event happens, the event bus is notified, 

which in turn will notify all relevant subscribers. It's not difficult at all to program a simple event bus yourself. For example, here's an implementation in only a few lines of code:

```php
interface Subscriber

{

    public function handles(object $event): bool;

    public function handle(object $event): void;

}

class EventBus

{

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

```

You can come up with lots of niceties and additions, but at its very core, this is all you need: a list of subscribers that can be notified whenever an event is dispatched.

Asynchronous Nothing is stopping you from making such an event bus asynchronous. In fact, 

an event-driven system is often preferred when doing async programming: it's a model that fits the parallel and async mindset extremely well.For our examples, we'll assume the event bus always processes events syn -

chronously: it's much simpler to reason about the event flow that way and elimi -

nate many technicalities we'd have to deal with otherwise.

In our invoice example, we'd have two services that subscribe to the InvoiceCreatedEvent  event:

```php
class InvoicePdfService implements Subscriber

{

    public function handles(object $event): bool

    {

        return $event instanceof InvoiceCreatedEvent;

    }

    public function handle(object $event): void

    {

```

        // Generate invoice PDF and save it on the filesystem

```php
    }

}

class InvoiceMailService implements Subscriber 

{ 

    public function handles(object $event): bool

    {

        return $event instanceof InvoiceCreatedEvent;

    }

    public function handle(object $event): void

    {

```

        // Send mail with a link to the customer's invoice page

```php
    }

}

```

Our implementation could do with a little polishing, though. By adding some reflection capabilities to our event bus, we can determine whether a subscriber should handle an event based on its method signature instead. This not only makes our code more concise, but also allows us to know exactly what kind of event we're dealing with in our subscribers. Let's imagine we've refactored our event bus, and can now write subscribers like so:

```php
class InvoicePdfService

{

   public function handle(InvoiceCreatedEvent $event): void

   {

```

        // Generate invoice PDF and save it on the filesystem

```php
   }

}

```

Let's continue exploring our event-driven system in depth. There's one big caveat with it - in fact, it's the major characteristic of all event-driven systems: indirectness.Imagine the invoice creation the InvoiceCreatedEvent  being triggered after the invoice was created:

```php
public function createInvoice()

{
$invoice = /* … */;
$event = new InvoiceCreatedEvent($invoice);
$this=>eventBus=>dispatch($event);

}

```

While event-driven development promises flexibility — you can hook up as many sub -

scribers as you want — it also causes a form on indirect coupling. We don't know what exactly will happen when we're triggering this event; we need to trust that the right subscribers will handle it without us seeing. This layer of indirectness can make de -

bugging the program flow much harder, even when events are handled synchronously. 

On top of that: you can't have any direct return value after dispatching an event, since an infinite amount of subscribers can handle that event. However, you could introduce some polling layer to observe the results in, for example, a database. Still, there are many complications you have to deal with: flexibility at the cost of simplicity.

Did you notice that we haven't written any "event sourcing" or "CQRS" code, yet still, 

we're already working with an event-driven program?. You don't need event sourcing, 

a command bus, CQRS, or micro services in its simplest form. You only need events. 

Given enough time, though, any developer working in such an event-driven system would encounter problems with this simplified approach.

There could be a wide range of performance issues: degraded developer experience, 

scaling issues, or problems with managing consistency and state. You would naturally try to solve those problems by applying patterns and principles, and that's exactly what the event-driven community has been doing for years now. They have come up with patterns to help tackle the more difficult problems, the ones you'd encounter in real-life, complex systems.

Martin Fowler writes and talks about several such patterns, and how the community discovered them. In the next part of this chapter, I will briefly discuss four of those patterns, all of which are often used. The relevant links are listed at the end of this chapter.

Event Notification The simplest form of an event-driven system called "Event Notification": events are merely used to notify about something that has happened. Our example with the InvoiceCreatedEvent  is already more complex than this since we're using the request data and sending it along with the event.

With event notifications, the event only signifies that something happened. It's up to the services themselves to reach out to the database, a third-party service, or outer state and determine what data they want to use. This is also the weakest form of event-driven development: everything is still coupled together. The only difference is that you're using the flexibility of events to hook several services up to one event.

Event-Carried State Transfer The second pattern is what we have applied in our example: we've captured the relevant data when the event occurred and sent it together with the event. All ser -

vices handling that event are only allowed to use the data that's encapsulated by that event.This approach ensures that we can have multiple services listening to the same event and don't have to worry about which order they are handled in. We're always sure our services won't rely on the external state, so the event becomes "a source of truth".

Event Sourcing Built upon the idea of events carrying all necessary state comes event sourcing. 

Instead of saving, for example, an invoice to the database, what would happen if we'd save the events themselves? Would that be beneficial?

If events become the source of truth and are saved to the database, there's a layer of extra information available to us at all times. Instead of knowing how the end result looks (the invoice), we now also know what the steps were that constituted that result 

(the events).

Take a look at this list of events, also called an "event stream":

[

    InvoiceDraftCreated=:class,

    InvoiceSent=:class,

    InvoicePaid=:class,

]

If we used events only to trigger a service to do something, we'd lose the event's data after it was handled. Traditional applications often deal with these kinds of problems, which is why they keep track of state changes in the database: columns like created_at  or payment_date  are added on the invoice and have to be carefully managed from there on out.

If we're saving the events directly, though, we can retrieve them from a store (a database, filesystem, or something else), and rebuild our application state dynami -

cally from scratch. For example, we can rebuild the invoice that would be the result of these events - at least as long as those stored events carry all the relevant data with them.

That's the power of event sourcing: being able to rebuild the whole application state, 

only by using events. It opens doors for interesting use cases. We could, for example, 

start generating reports based on the historical data that's available within these events. We could generate a report that analyses the average time it takes for customers to pay their invoice after it was sent to them, without rewriting our data model. 

That's right: all the data we need is already stored as events, we just need to interpret them in a new way.

With event sourcing come lots of other problems, though. The most pressing one: 

performance. A production application will store millions upon millions of events over time; surely, we can't rebuild our whole application state from scratch every time a request comes in. That's why there are other patterns helping us with those kinds of problems: projections and snapshots are often used to build a cached and reusable state, instead of always rebuilding it from scratch. A practical example could be an invoice projection: a table that stores the end result of all those invoice events and where we can easily read data from.

Another abstraction that often comes with event sourcing is the difference between the intention of making a change, and the change itself. When we directly triggered an InvoiceCreatedEvent , it felt a little off: the invoice itself wasn't created yet . Instead it would make more sense to have the intent called CreateInvoice  and the actual result to store in the database InvoiceCreated . The first one is often called the "command", 

```php
while the second one is called the "event".

```

A lot of complexity appears when we're trying to apply event sourcing properly. That's because of the same reasons our most basic implementation also added complexity: it's the cost we pay for a more flexible and scalable system. Keep this in mind: anevent-driven architecture isn't always the right solution for a problem. It might very well be that a simpler approach is not only faster but also better.

A wise developer, Frank De Jonge, once said: "Event Sourcing makes simple problems hard, and hard problems simple" . Make sure you've weighed the pros and cons before adding event sourcing to your project.

CQRS CQRS — command query responsibility segregation — is the fourth and final pattern I want to touch on. Martin Fowler describes it like this: "At its heart is the notion that you can use a different model to update information than the model you use to read information. For some situations, this separation can be valuable […] The rationale is that for many problems, particularly in more complicated domains, having the same conceptual model for commands and queries leads to a more complex model that does neither well."

In other words: CQRS aims to separate the concerns of writing data and reading data. 

It again allows for more flexibility. Keep in mind that it's a pattern for very complex systems. Martin Fowler even warns not to use CQRS too quickly: "Despite these bene -

fits, you should be very cautious about using CQRS. Many information systems fit well with the notion of an information base that is updated in the same way that it's read, 

adding CQRS to such a system can add significant complexity."

There's lots more to tell about event-driven systems, but it's outside the scope of this book. Several PHP frameworks facilitate an event-driven system, but most important is the event-driven mindset instead of a bunch of technical tools. I hope you've got a bit of an idea of what that mindset consists of, and I recommend checking out some more resources on the topic if you're interested in it.

Some More Resources Martin Fowler's introduction to event-driven architecture: https://www.youtube.

com/watch?v=STKCRSUsyP0 Greg Young sharing insights on DDD, CQRS and Event Sourcing: https://www.

youtube.com/watch?v=LDW0QWie21s
