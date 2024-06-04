const JamonDecorator = require('../src/JamonDecorator');
const AceitunaDecorator = require('../src/AceitunaDecorator');
const PizzaBase = require('../src/PizzaBase');

    test("Pizza",()=> {
      const pizzaBase= new PizzaBase();
      expect(pizzaBase.getName()).toBe("Pizza")
      expect(pizzaBase.getPrice()).toBe(10)
      expect(pizzaBase.getDescription()).toBe("Masa-Salsa-Queso")
    })

    test("JamonDecorator",()=> {
      const pizzaBase= new PizzaBase();
      const pizzaJamon= new JamonDecorator(pizzaBase);
      expect(pizzaJamon.getName()).toBe("Pizza con Jamon")
      expect(pizzaJamon.getPrice()).toBe(12)
      expect(pizzaJamon.getDescription()).toBe("Masa-Salsa-Queso-Jamon")
    })

    test("Jamon y aceitunas",()=> {
      const pizzaBase= new PizzaBase();
      const pizzaJamon= new JamonDecorator(pizzaBase);
      const pizzaJamonYAceitunas= new AceitunaDecorator(pizzaJamon)
      expect(pizzaJamonYAceitunas.getName()).toBe("Pizza con Jamon con aceitunas")
      expect(pizzaJamonYAceitunas.getPrice()).toBe(13)
      expect(pizzaJamonYAceitunas.getDescription()).toBe("Masa-Salsa-Queso-Jamon-Aceitunas")
    })
