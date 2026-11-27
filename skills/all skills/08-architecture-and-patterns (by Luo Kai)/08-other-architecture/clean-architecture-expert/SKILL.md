---
author: luo-kai
name: clean-architecture
description: Expert-level Clean Architecture and SOLID principles. Use when structuring codebases with clean architecture, applying SOLID principles, dependency inversion, use cases, ports and adapters, hexagonal architecture, or onion architecture. Also use when the user mentions 'Clean Architecture', 'SOLID', 'dependency inversion', 'hexagonal', 'use case', 'ports and adapters', 'domain layer', 'application layer', or 'Uncle Bob'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Clean Architecture Expert

You are an expert in Clean Architecture, SOLID principles, and software design with deep knowledge of structuring codebases for long-term maintainability and testability.

## Before Starting

1. **Language/framework** — Python, TypeScript, Java, Go, C#?
2. **Current state** — greenfield, refactoring existing code, or code review?
3. **Problem type** — folder structure, dependency issues, testing difficulty, SOLID violation?
4. **Team experience** — familiar with clean architecture or learning?
5. **Scale** — small app, medium product, large enterprise system?

---

## Core Expertise Areas

- **The Dependency Rule**: dependencies always point inward, never outward
- **Layers**: entities, use cases, interface adapters, frameworks and drivers
- **SOLID principles**: SRP, OCP, LSP, ISP, DIP — in practice not just theory
- **Ports and adapters**: hexagonal architecture, primary/secondary adapters
- **Use cases**: application business rules, interactors, command/query handlers
- **Entities**: enterprise business rules, domain objects, pure business logic
- **Dependency injection**: constructor injection, DI containers, composition root
- **Testing**: testability by design, test each layer independently

---

## Key Patterns & Code

### The Dependency Rule
```
Clean Architecture layers (outer to inner):

  +--------------------------------------------------+
  |  Frameworks & Drivers                            |
  |  (Web, DB, UI, External APIs)                   |
  |  +--------------------------------------------+ |
  |  |  Interface Adapters                        | |
  |  |  (Controllers, Presenters, Gateways)       | |
  |  |  +--------------------------------------+  | |
  |  |  |  Application Business Rules          |  | |
  |  |  |  (Use Cases / Interactors)           |  | |
  |  |  |  +--------------------------------+  |  | |
  |  |  |  |  Enterprise Business Rules     |  |  | |
  |  |  |  |  (Entities / Domain Objects)   |  |  | |
  |  |  |  +--------------------------------+  |  | |
  |  |  +--------------------------------------+  | |
  |  +--------------------------------------------+ |
  +--------------------------------------------------+

The Dependency Rule:
  Source code dependencies ONLY point inward
  Inner layers know NOTHING about outer layers
  Entities know nothing about use cases
  Use cases know nothing about controllers or databases
  Controllers know nothing about Express, FastAPI, etc.

What crosses boundaries:
  Data crosses boundaries as simple data structures (DTOs)
  NEVER pass framework objects (Request, Response) to use cases
  NEVER pass database entities to outer layers
```

### Folder Structure
```
src/
  domain/                    # Enterprise Business Rules
    entities/
      user.ts                # Domain entity — pure business logic
      order.ts
    value-objects/
      email.ts               # Validated value object
      money.ts
    errors/
      domain-errors.ts       # Domain-specific errors
    repositories/
      user-repository.ts     # Repository INTERFACE (port)
      order-repository.ts

  application/               # Application Business Rules
    use-cases/
      create-user/
        create-user.usecase.ts
        create-user.dto.ts
        create-user.test.ts
      get-user/
        get-user.usecase.ts
        get-user.dto.ts
      place-order/
        place-order.usecase.ts
        place-order.dto.ts
    ports/
      email-service.port.ts  # Output port (interface)
      payment-gateway.port.ts
      event-publisher.port.ts

  infrastructure/            # Frameworks & Drivers (adapters)
    database/
      prisma-user-repository.ts   # Implements domain/repositories/user-repository
      prisma-order-repository.ts
    email/
      sendgrid-email-service.ts   # Implements application/ports/email-service.port
    payment/
      stripe-payment-gateway.ts
    http/
      express-server.ts
      controllers/
        user.controller.ts
        order.controller.ts
    events/
      kafka-event-publisher.ts

  main/                      # Composition Root — wires everything together
    container.ts
    app.ts
```

### Domain Entities — Pure Business Logic
```typescript
// domain/entities/user.ts
// NO imports from infrastructure, frameworks, or databases
// Pure TypeScript — no decorators, no ORM annotations

import { Email } from '../value-objects/email';
import { DomainError } from '../errors/domain-errors';

export interface UserProps {
  id: string;
  email: Email;
  name: string;
  role: UserRole;
  createdAt: Date;
  isActive: boolean;
}

export type UserRole = 'user' | 'moderator' | 'admin';

export class User {
  private readonly props: UserProps;

  private constructor(props: UserProps) {
    this.props = props;
  }

  // Factory method — validates invariants before creating
  static create(props: Omit<UserProps, 'createdAt' | 'isActive'>): User {
    if (!props.name || props.name.trim().length < 2) {
      throw new DomainError('User name must be at least 2 characters');
    }
    return new User({
      ...props,
      createdAt: new Date(),
      isActive: true,
    });
  }

  // Reconstitute from persistence
  static reconstitute(props: UserProps): User {
    return new User(props);
  }

  // Getters — controlled access to state
  get id(): string { return this.props.id; }
  get email(): Email { return this.props.email; }
  get name(): string { return this.props.name; }
  get role(): UserRole { return this.props.role; }
  get isActive(): boolean { return this.props.isActive; }

  // Business methods — domain logic lives here
  promote(requestedBy: User): void {
    if (!requestedBy.isAdmin()) {
      throw new DomainError('Only admins can promote users');
    }
    if (this.props.role === 'admin') {
      throw new DomainError('User is already an admin');
    }
    this.props.role = 'admin';
  }

  deactivate(): void {
    if (!this.props.isActive) {
      throw new DomainError('User is already inactive');
    }
    this.props.isActive = false;
  }

  isAdmin(): boolean {
    return this.props.role === 'admin';
  }
}

// domain/value-objects/email.ts
export class Email {
  private readonly value: string;

  private constructor(value: string) {
    this.value = value;
  }

  static create(raw: string): Email {
    const normalized = raw.trim().toLowerCase();
    if (!normalized.includes('@') || !normalized.includes('.')) {
      throw new DomainError('Invalid email format: ' + raw);
    }
    if (normalized.length > 255) {
      throw new DomainError('Email too long');
    }
    return new Email(normalized);
  }

  toString(): string { return this.value; }
  equals(other: Email): boolean { return this.value === other.value; }
}
```

### Repository Port (Interface)
```typescript
// domain/repositories/user-repository.ts
// This is a PORT — defined in the domain layer
// The domain layer defines WHAT it needs, not HOW it is implemented

import { User } from '../entities/user';
import { Email } from '../value-objects/email';

export interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: Email): Promise<User | null>;
  save(user: User): Promise<void>;
  delete(id: string): Promise<void>;
  existsByEmail(email: Email): Promise<boolean>;
}
```

### Use Case
```typescript
// application/use-cases/create-user/create-user.usecase.ts
// Use cases orchestrate domain objects and call ports
// They know about entities and ports, but NOT about databases or HTTP

import { User, UserRole } from '../../../domain/entities/user';
import { Email } from '../../../domain/value-objects/email';
import { UserRepository } from '../../../domain/repositories/user-repository';
import { EmailServicePort } from '../../ports/email-service.port';
import { CreateUserDto, CreateUserResultDto } from './create-user.dto';
import { DomainError } from '../../../domain/errors/domain-errors';

export class CreateUserUseCase {
  constructor(
    private readonly userRepository: UserRepository,      // injected port
    private readonly emailService: EmailServicePort,      // injected port
  ) {}

  async execute(dto: CreateUserDto): Promise<CreateUserResultDto> {
    // Parse and validate value objects
    const email = Email.create(dto.email);

    // Business rule: email must be unique
    const exists = await this.userRepository.existsByEmail(email);
    if (exists) {
      throw new DomainError('Email already registered: ' + dto.email);
    }

    // Create domain entity
    const user = User.create({
      id: crypto.randomUUID(),
      email,
      name: dto.name,
      role: 'user' as UserRole,
    });

    // Persist via repository port
    await this.userRepository.save(user);

    // Send welcome email via email port
    await this.emailService.sendWelcome({
      to: user.email.toString(),
      name: user.name,
    });

    // Return DTO — not the domain entity
    return {
      id: user.id,
      email: user.email.toString(),
      name: user.name,
      createdAt: user.createdAt,
    };
  }
}

// application/use-cases/create-user/create-user.dto.ts
export interface CreateUserDto {
  name: string;
  email: string;
  password: string;
}

export interface CreateUserResultDto {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}
```

### Infrastructure Adapter
```typescript
// infrastructure/database/prisma-user-repository.ts
// This adapter implements the domain repository port
// It knows about Prisma, but the domain knows nothing about Prisma

import { PrismaClient } from '@prisma/client';
import { User } from '../../domain/entities/user';
import { Email } from '../../domain/value-objects/email';
import { UserRepository } from '../../domain/repositories/user-repository';

export class PrismaUserRepository implements UserRepository {
  constructor(private readonly prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    const row = await this.prisma.user.findUnique({ where: { id } });
    if (!row) return null;
    return this.toDomain(row);
  }

  async findByEmail(email: Email): Promise<User | null> {
    const row = await this.prisma.user.findUnique({
      where: { email: email.toString() }
    });
    if (!row) return null;
    return this.toDomain(row);
  }

  async save(user: User): Promise<void> {
    await this.prisma.user.upsert({
      where: { id: user.id },
      create: this.toPersistence(user),
      update: this.toPersistence(user),
    });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({ where: { id } });
  }

  async existsByEmail(email: Email): Promise<boolean> {
    const count = await this.prisma.user.count({
      where: { email: email.toString() }
    });
    return count > 0;
  }

  // Map DB row to domain entity
  private toDomain(row: any): User {
    return User.reconstitute({
      id: row.id,
      email: Email.create(row.email),
      name: row.name,
      role: row.role,
      createdAt: row.createdAt,
      isActive: row.isActive,
    });
  }

  // Map domain entity to DB row
  private toPersistence(user: User): any {
    return {
      id: user.id,
      email: user.email.toString(),
      name: user.name,
      role: user.role,
      createdAt: user.createdAt,
      isActive: user.isActive,
    };
  }
}
```

### HTTP Controller (Interface Adapter)
```typescript
// infrastructure/http/controllers/user.controller.ts
// Controllers translate HTTP requests to use case DTOs
// They know about Express/Fastify but use cases know nothing about HTTP

import { Request, Response } from 'express';
import { CreateUserUseCase } from '../../../application/use-cases/create-user/create-user.usecase';
import { DomainError } from '../../../domain/errors/domain-errors';

export class UserController {
  constructor(
    private readonly createUser: CreateUserUseCase,
  ) {}

  async handleCreateUser(req: Request, res: Response): Promise<void> {
    try {
      // Translate HTTP request to use case DTO
      const result = await this.createUser.execute({
        name: req.body.name,
        email: req.body.email,
        password: req.body.password,
      });

      // Translate use case result to HTTP response
      res.status(201).json({
        data: result,
        message: 'User created successfully',
      });
    } catch (error) {
      if (error instanceof DomainError) {
        res.status(422).json({ error: error.message });
        return;
      }
      res.status(500).json({ error: 'Internal server error' });
    }
  }
}
```

### Composition Root
```typescript
// main/container.ts — wires everything together
// This is the ONLY place that knows about all layers

import { PrismaClient } from '@prisma/client';
import { PrismaUserRepository } from '../infrastructure/database/prisma-user-repository';
import { SendGridEmailService } from '../infrastructure/email/sendgrid-email-service';
import { CreateUserUseCase } from '../application/use-cases/create-user/create-user.usecase';
import { UserController } from '../infrastructure/http/controllers/user.controller';

export function buildContainer() {
  // Infrastructure
  const prisma = new PrismaClient();
  const userRepository = new PrismaUserRepository(prisma);
  const emailService = new SendGridEmailService(process.env.SENDGRID_API_KEY!);

  // Use Cases
  const createUserUseCase = new CreateUserUseCase(userRepository, emailService);

  // Controllers
  const userController = new UserController(createUserUseCase);

  return { userController, prisma };
}
```

### Testing Use Cases in Isolation
```typescript
// application/use-cases/create-user/create-user.test.ts
// Use cases are tested with fake/mock repositories — no DB, no HTTP

import { CreateUserUseCase } from './create-user.usecase';
import { UserRepository } from '../../../domain/repositories/user-repository';
import { EmailServicePort } from '../../ports/email-service.port';
import { DomainError } from '../../../domain/errors/domain-errors';

// In-memory fake repository
class InMemoryUserRepository implements UserRepository {
  private users = new Map<string, any>();

  async findById(id: string) {
    return this.users.get(id) ?? null;
  }

  async findByEmail(email: any) {
    for (const user of this.users.values()) {
      if (user.email.toString() === email.toString()) return user;
    }
    return null;
  }

  async save(user: any) {
    this.users.set(user.id, user);
  }

  async delete(id: string) {
    this.users.delete(id);
  }

  async existsByEmail(email: any) {
    for (const user of this.users.values()) {
      if (user.email.toString() === email.toString()) return true;
    }
    return false;
  }
}

// Fake email service
class FakeEmailService implements EmailServicePort {
  public sentEmails: any[] = [];

  async sendWelcome(params: any) {
    this.sentEmails.push(params);
  }
}

describe('CreateUserUseCase', () => {
  let useCase: CreateUserUseCase;
  let userRepo: InMemoryUserRepository;
  let emailService: FakeEmailService;

  beforeEach(() => {
    userRepo = new InMemoryUserRepository();
    emailService = new FakeEmailService();
    useCase = new CreateUserUseCase(userRepo, emailService);
  });

  it('should create a user and return their data', async () => {
    const result = await useCase.execute({
      name: 'Alice',
      email: 'alice@example.com',
      password: 'securepassword',
    });

    expect(result.email).toBe('alice@example.com');
    expect(result.name).toBe('Alice');
    expect(result.id).toBeDefined();
  });

  it('should send a welcome email after creation', async () => {
    await useCase.execute({
      name: 'Alice',
      email: 'alice@example.com',
      password: 'securepassword',
    });

    expect(emailService.sentEmails).toHaveLength(1);
    expect(emailService.sentEmails[0].to).toBe('alice@example.com');
  });

  it('should throw DomainError when email already exists', async () => {
    await useCase.execute({ name: 'Alice', email: 'alice@example.com', password: 'pass' });

    await expect(
      useCase.execute({ name: 'Bob', email: 'alice@example.com', password: 'pass' })
    ).rejects.toThrow(DomainError);
  });
});
```

### SOLID in Practice
```typescript
// S — Single Responsibility Principle
// Each class has ONE reason to change

// Bad: UserService does too many things
class UserService {
  createUser() {}      // user creation logic
  sendEmail() {}       // email sending
  saveToDatabase() {}  // database operations
  validateInput() {}   // input validation
  hashPassword() {}    // password hashing
}

// Good: each class has one responsibility
class UserRepository { save(user: User) {} }
class EmailService { sendWelcome(email: string) {} }
class PasswordHasher { hash(password: string) {} }
class CreateUserUseCase { execute(dto: CreateUserDto) {} }

// O — Open/Closed Principle
// Open for extension, closed for modification

// Bad: adding new payment method requires modifying PaymentService
class PaymentService {
  process(method: string, amount: number) {
    if (method === 'stripe') { /* stripe logic */ }
    else if (method === 'paypal') { /* paypal logic */ }
    // Every new method requires modifying this class
  }
}

// Good: extend by adding new classes
interface PaymentGateway { charge(amount: number): Promise<string>; }
class StripeGateway implements PaymentGateway { async charge(amount) { return 'stripe_id'; } }
class PaypalGateway implements PaymentGateway { async charge(amount) { return 'paypal_id'; } }
class PaymentService {
  constructor(private gateway: PaymentGateway) {}
  async process(amount: number) { return this.gateway.charge(amount); }
}

// D — Dependency Inversion Principle
// Depend on abstractions, not concretions

// Bad: use case depends on concrete Prisma repository
class CreateUserUseCase {
  private repo = new PrismaUserRepository(); // concrete dependency
}

// Good: use case depends on interface
class CreateUserUseCase {
  constructor(private repo: UserRepository) {} // abstract dependency
}
```

---

## Best Practices

- Start simple — do not add layers until you feel the pain of not having them
- The domain layer must have zero external dependencies — no ORMs, no frameworks
- Use cases should be thin orchestrators — business logic belongs in entities
- Always return DTOs from use cases — never expose domain entities to outer layers
- Composition root is the only place that creates concrete implementations
- Name use cases after user intentions: CreateUser, PlaceOrder, CancelSubscription
- Test use cases with in-memory fakes, not mocks — fakes are more reliable
- Interfaces belong in the layer that uses them, not the layer that implements them

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Anemic domain model | Entities are just data bags, logic is in services | Move business rules into entity methods |
| Use cases doing too much | Fat use cases, thin entities | Push logic to domain entities and value objects |
| Framework in domain | Domain imports from Express, Prisma, etc. | Domain has zero external imports |
| Passing ORM entities across layers | Leaks infrastructure details to domain | Map to domain entities in repository adapter |
| Skipping layers | Controller calls repository directly | Always go through use case |
| Over-engineering small apps | 6 layers for a TODO app | Match complexity to actual needs |
| Interface in wrong layer | Repository interface defined in infrastructure | Interfaces belong in domain layer |
| No composition root | Dependencies created everywhere | Single place wires all dependencies |

---

## Related Skills

- **domain-driven-design**: For domain modeling and bounded contexts
- **design-patterns**: For patterns used within clean architecture
- **testing-expert**: For testing each layer independently
- **typescript-expert**: For TypeScript interfaces and dependency injection
- **microservices-expert**: For clean architecture across services
- **api-design-expert**: For designing the interface adapter layer