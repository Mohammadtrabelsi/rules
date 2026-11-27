[Rules index](../README.md) › Stack mapping

**Navigation:** Previous: [AI agent prompt](../ai-agents/README.md) · Next: [Proposed rules](../general/proposed-rules.md) · [Table of contents](../README.md#table-of-contents)

# Stack mapping

The rules in this repository name no framework, language or product. They describe the work: a service layer, an authorization check, a migration, a rate limit. This page is the only place that says how each concept looks in a real stack.

Use it to translate a rule into your project. A rule that says "the service layer" is satisfied by a `services/` folder in one stack and by `@Service` classes in another, as long as the check it describes holds.

This page is exempt from the framework-name check in `tools/check_rules.py`. Nothing else is.

---

## Concept map

| Concept (as used in the rules) | Laravel (PHP) | Django (Python) | Ruby on Rails | Express or NestJS (Node.js) | Spring Boot (Java) | ASP.NET Core (C#) |
|---|---|---|---|---|---|---|
| Service layer | `app/Services/` | `services.py` or `services/` | `app/services/` | `src/services/` or NestJS providers | `@Service` classes | service classes registered for DI |
| Dependency injection | constructor injection | services passed in as arguments (or a DI package) | service objects passed in as arguments | NestJS constructor injection; plain Express passes services as arguments | constructor injection | built-in DI container |
| Authorization rule | Policies and Gates | permissions and `has_perm` | Pundit or CanCanCan | middleware or guards | `@PreAuthorize` | `[Authorize(Policy = ...)]` |
| Rate limiter | `RateLimiter::for()` and `throttle:` | django-ratelimit or DRF throttling | Rack::Attack | express-rate-limit or `@nestjs/throttler` | Bucket4j or a gateway | `AddRateLimiter` |
| Soft delete | `SoftDeletes` trait | django-safedelete or a `deleted_at` manager | Paranoia or Discard | Sequelize `paranoid`, or a `deletedAt` column | `@SQLDelete` and `@SQLRestriction` | global query filter on `IsDeleted` |
| Audit log | spatie/laravel-activitylog | django-simple-history | PaperTrail or audited | an audit table written in a hook | Hibernate Envers | EF Core interceptors or audit tables |
| Eager loading | `with()` | `select_related`, `prefetch_related` | `includes` | `include` (Prisma, Sequelize) | `JOIN FETCH`, `@EntityGraph` | `Include` |
| N+1 detection | `Model::preventLazyLoading()` | django-zen-queries or nplusone | `strict_loading`, Bullet | query logging in tests | Hibernate statistics | EF Core query logging |
| Transaction | `DB::transaction()` | `transaction.atomic` | `ActiveRecord::Base.transaction` | `prisma.$transaction` or a Sequelize transaction | `@Transactional` | `BeginTransactionAsync` |
| Background jobs | queued jobs and listeners | Celery | Active Job with Sidekiq | BullMQ | Spring `@Async`, Quartz or a broker | Hangfire or hosted services |
| Migrations | `php artisan make:migration` | `makemigrations` and `migrate` | `rails generate migration` | Prisma Migrate, Knex or TypeORM | Flyway or Liquibase | EF Core migrations |
| Formatter and analyzer | Pint and PHPStan (Larastan) | Black or Ruff, plus mypy | RuboCop | Prettier and ESLint, `tsc --noEmit` | Spotless and SpotBugs | `dotnet format` and Roslyn analyzers |
| Test runner | Pest or PHPUnit | pytest or Django's test runner | RSpec or Minitest | Jest or Vitest | JUnit 5 with Mockito | xUnit or NUnit |
| Translation bundles | `lang/{locale}/{feature}.php` | gettext `.po` files | `config/locales/*.yml` | i18next namespaces (JSON) | `messages_xx.properties` | `.resx` resource files |
| Missing-key check | `translations:sync` (laravel-translation-sync) | `makemessages` diff | i18n-tasks | i18next-parser | a test that loads every bundle | a test that loads every resource |
| Templates | `resources/views/` | `templates/` | `app/views/` | EJS, Pug or React components | Thymeleaf | Razor `.cshtml` views |
| Server-driven updates | Livewire | htmx | Hotwire (Turbo) | Hotwire or htmx | htmx or Thymeleaf fragments | Blazor or htmx |
| Dependency audit | `composer audit`, `npm audit` | `pip-audit` | `bundle audit` | `npm audit` | OWASP Dependency-Check | `dotnet list package --vulnerable` |

Names are examples, not requirements. Pick the tool your team already uses and keep the same check.

---

## Self-check settings per stack

The self-check in [Testing](../testing/testing.md#self-check-before-finishing) and in [`ai-agents/CLAUDE.md`](../ai-agents/CLAUDE.md) reads three variables. Set them once in the project, then run the block.

| Stack | `TEMPLATES` | `HANDLERS` | `DATA_ACCESS_RE` |
|---|---|---|---|
| Laravel | `resources/views` | `app/Http/Controllers app/Livewire` | `DB::\|::where\(\|::find\(\|::create\(\|::all\(\|::first\(` |
| Django | `templates` | `myapp/views` | `\.objects\.` |
| Rails | `app/views` | `app/controllers` | `\.(where\|find_by\|create!?\|destroy)\(` |
| Express or NestJS | `views` | `src/controllers src/routes` | `prisma\.\|\.query\(` |
| Spring Boot | `src/main/resources/templates` | `src/main/java/*/web` | `Repository\|EntityManager\|JdbcTemplate` |
| ASP.NET Core | `Views` | `Controllers` | `DbContext\|SaveChanges` |

Each pattern is an extended regular expression for `grep -E`. The table escapes every `|` as `\|` so the Markdown table does not break; in your shell variable, write a plain `|`. The handler folders may be a space-separated list or a glob, because the self-check expands `$HANDLERS` without quotes.

---

## Examples in one stack

The rules show neutral pseudo-code. These are the same ideas written for Laravel, which is where several of the rules were first worked out.

**Rate limiter** (rule: named, configurable, keyed by form and address)

```php
// app/Providers/AppServiceProvider.php
RateLimiter::for('contact', function (Request $request): Limit {
    return Limit::perMinute(config('site.form_throttle.contact', 10))
        ->by('contact|'.$request->ip());
});

// routes/web.php
Route::post('contact', ContactController::class)->middleware('throttle:contact');
```

**Authorization rule** (rule: check on the server, not only in the UI)

```php
final class PaymentPolicy
{
    public function refund(User $user, Payment $payment): bool
    {
        return $user->can('payments.refund') && $user->tenant_id === $payment->tenant_id;
    }
}

// In the component or controller
$this->authorize('refund', $this->payment);
```

**Enum for a status** (rule: a typo in a status is impossible)

```php
enum InvoiceStatus: string
{
    case Draft = 'draft';
    case Sent = 'sent';
    case Paid = 'paid';
}
```

**Soft delete** (rule: financial records are never permanently deleted)

```php
final class Payment extends Model
{
    use SoftDeletes;
}
```

**Transaction** (rule: multi-step writes succeed or fail together)

```php
public function recordPayment(Invoice $invoice, int $amountMinor): Payment
{
    return DB::transaction(function () use ($invoice, $amountMinor): Payment {
        $payment = $invoice->payments()->create(['amount_minor' => $amountMinor]);
        $invoice->update(['status' => InvoiceStatus::Paid]);

        return $payment;
    });
}
```

For the same ideas in another stack, read the table above and then the framework's own documentation for that feature. The rule stays the same; only the names change.

---

## Static sites and no framework

A site with plain HTML and a little JavaScript has no service layer or ORM. The rules still apply where they can:

- **Templates:** the page files are the templates. The inline script, inline style and table checks apply unchanged.
- **Data:** if the page reads data from an API, the API owns the rules in [Security](../security/security.md) and [Data and performance](../backend/data-and-performance.md).
- **Rate limiting and headers:** set them at the host, the CDN or the reverse proxy, and record the setting in the project.
- **Translations:** one JSON file per locale, with the same key check.

---

**Related:** [Architecture](../architecture/layering-and-patterns.md) · [Testing](../testing/testing.md) · [Summary](../SUMMARY.md)
