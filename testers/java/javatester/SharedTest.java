package javatester;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.lang.reflect.Type;
import java.lang.reflect.TypeVariable;
import java.util.Arrays;
import java.util.stream.Collectors;

public class SharedTest {

  public static final int TIMEOUT = 1000;
  public static final double EPSILON = 0.01;

  public static void shouldBeAbsrtact(Class<?> cls) {
    assertTrue(String.format("%s should be an abstract class", cls.getName()),
        Modifier.isAbstract(cls.getModifiers()));
  }

  public static void shouldBeAbsrtact(Method method) {
    assertTrue(String.format("%s should be an abstract method", method.getName()),
        Modifier.isAbstract(method.getModifiers()));
  }

  public static void shouldBeDefault(Method method) {
    assertTrue(String.format("%s should be a default method", method.getName()),
        method.isDefault());
  }

  public static void shouldBeInterface(Class<?> cls) {
    assertTrue(String.format("%s should be an interface", cls.getName()), cls.isInterface());
  }

  public static void shouldNotBeInterface(Class<?> cls) {
    assertFalse(String.format("%s should not be an interface", cls.getName()), cls.isInterface());
  }

  public static void shouldBeGeneric(Class<?> cls) {
    assertTrue(String.format("%s should be generic", cls.getName()),
        cls.getTypeParameters().length > 0);
  }

  public static void shouldNotBeGeneric(Class<?> cls) {
    assertEquals(String.format("%s should be generic", cls.getName()),
        cls.getTypeParameters().length, 0);
  }

  public static void shouldHaveTypeParameter(Class<?> cls, Class<?> param) {
    TypeVariable<?>[] tvs = cls.getTypeParameters();
    assertTrue(String.format("%s should have %s as type parameter", cls.getName(), param.getName()),
        Arrays.asList(tvs).stream().anyMatch(t -> t.getClass().equals(param.getClass())));
  }

  public static TypeVariable<?>[] shouldHaveNTypeParameters(Class<?> cls, int n) {
    TypeVariable<?>[] tvs = cls.getTypeParameters();
    assertEquals(String.format("%s should have %d type parameters", cls.getName(), n),
        tvs.length, n);
    return tvs;
  }

  public static void shouldContainBooleanField(Class<?> cls) {
    shouldContainFieldEither(cls, Boolean.class, boolean.class);
  }

  public static void shouldContainDoubleField(Class<?> cls, boolean only) {
    shouldContainFieldEither(cls, Double.class, double.class);
  }

  /**
   * Check that cls contains field.
   *
   * @param cls   class
   * @param field field
   */
  public static void shouldContainField(Class<?> cls, Class<?> field) {
    boolean present = Arrays.asList(cls.getDeclaredFields()).stream()
        .anyMatch(fld -> fld.getType().equals(field));
    String msg = String.format("%s should have a field of type %s", cls.getName(), field.getName());
    assertTrue(msg, present);
  }

  public static void onlyPrivateFields(Class<?> cls) {
    boolean allPrivate = Arrays.asList(cls.getDeclaredFields()).stream()
        .allMatch(fld -> Modifier.isPrivate(fld.getModifiers()));
    String msg = String.format("%s should have only private fields", cls.getName());
    assertTrue(msg, allPrivate);
  }

  private static void shouldContainFieldEither(Class<?> cls, Class<?> either, Class<?> or) {
    boolean present = Arrays.asList(cls.getDeclaredFields()).stream()
        .anyMatch(fld -> fld.getType().equals(either) || fld.getType().equals(or));
    String msg = String.format("%s should have a field of type %s/%s", cls.getName(),
        either.getName(), or.getName());
    assertTrue(msg, present);
  }

  public static Field[] shouldContainNFields(Class<?> cls, int n) {
    Field[] fields = cls.getDeclaredFields();
    assertTrue(String.format("%s should have %d field(s)", cls.getName(), n), fields.length == n);
    return fields;
  }

  public static Field[] shouldContainAtLeastNFields(Class<?> cls, int n) {
    Field[] fields = cls.getDeclaredFields();
    assertTrue(String.format("%s should have %d field(s)", cls.getName(), n), fields.length >= n);
    return fields;
  }

  // ** Implementing methods (excludes inherited) ***/
  public static Method[] shouldDeclareNMethods(Class<?> cls, int n) {
    Method[] methods = cls.getDeclaredMethods();
    assertEquals(String.format("%s should declare %d methods.", cls.getName(), n), n,
        methods.length);
    return methods;
  }

  public static Method[] shouldDeclareAtLeastNMethods(Class<?> cls, int n) {
    Method[] methods = cls.getDeclaredMethods();
    assertTrue(String.format("%s should declare %d methods.", cls.getName(), n),
        methods.length >= n);
    return methods;
  }

  public static Type shouldExtend(Class<?> cls, Class<?> parent) {
    Type parentType = cls.getSuperclass();
    assertTrue(String.format("%s should extend %s", cls.getName(), parent.getName()),
        parentType.equals(parent));
    return parentType;
  }

  public static Type shouldExtendGeneric(Class<?> cls, Class<?> parent) {
    Type parentType = cls.getGenericSuperclass();
    assertTrue(String.format("%s should extend %s", cls.getName(), parent.getName()),
        parentType.getTypeName().contains(parent.getName()));
    return parentType;
  }

  /**
   * Assert that cls has a constructor with params. Return this constructor.
   *
   * @param cls    class
   * @param params parameters
   * @return constructor if exists
   */
  public static Constructor<?> shouldHaveConstructor(Class<?> cls, Class<?>[] params) {
    try {
      return cls.getConstructor(params);
    } catch (NoSuchMethodException | SecurityException ex) {

      String msg = String.format("%s should implement constructor %s(%s)", cls.getName(),
          cls.getName(), paramsStr(params));
      fail(msg);
    }
    return null;
  }

  private static String paramsStr(Class<?>[] params) {
    return Arrays.asList(params).stream().map(p -> p.getClass().getName())
        .collect(Collectors.joining(", "));
  }

  /**
   * Assert that cls has a constructor with either parameters either or parameters
   * or. Return this constructor.
   *
   * @param cls    class
   * @param either or parameters
   * @return constructor if exists
   */
  public static Constructor<?> shouldHaveConstructorEither(Class<?> cls, Class<?>[] either,
      Class<?>[] or) {
    try {
      return cls.getConstructor(either);
    } catch (NoSuchMethodException | SecurityException e) {
      try {
        return cls.getConstructor(or);
      } catch (NoSuchMethodException | SecurityException ex) {
        String msg = String.format("%s should have constructor %s(%s) / %s(%s)", cls.getName(),
            cls.getName(), paramsStr(either), cls.getName(), paramsStr(or));
        fail(msg);
      }
    }
    return null;
  }

  /**
   * Asserts that cls has method name with parameters params: includes inherited
   * methods.
   *
   * @param cls    class
   * @param name   method name
   * @param params parameter
   * @return
   */
  public static Method shouldHaveMethod(Class<?> cls, String name, Class<?>[] params) {
    try {
      return cls.getMethod(name, params);
    } catch (NoSuchMethodException | SecurityException e) {
      String msg = String.format("%s should implement %s(%s)", cls.getName(), name,
          paramsStr(params));
      fail(msg);
    }
    return null;
  }

  public static Constructor<?>[] shouldHaveNConstructors(Class<?> cls, int n) {
    Constructor<?>[] constructors = cls.getConstructors();
    assertTrue(String.format("%s should have %d constructor(s)", cls.getName(), n),
        constructors.length == 1);
    return constructors;
  }

  public static Constructor<?> shouldHaveTakesBooleanConstructor(Class<?> cls) {
    return shouldHaveTakesEitherConstructor(cls, Boolean.class, boolean.class);
  }

  public static Method shouldHaveTakesBooleanMethod(Class<?> cls, String name) {
    return shouldHaveTakesEither(cls, Boolean.class, boolean.class, name);
  }

  public static Constructor<?> shouldHaveTakesDoubleConstructor(Class<?> cls) {
    return shouldHaveTakesEitherConstructor(cls, Double.class, double.class);
  }

  public static Method shouldHaveTakesDoubleMethod(Class<?> cls, String name) {
    return shouldHaveTakesEither(cls, Double.class, double.class, name);
  }

  private static Method shouldHaveTakesEither(Class<?> cls, Class<?> either, Class<?> or,
      String name) {
    try {
      return cls.getMethod(name, new Class<?>[] { either });
    } catch (NoSuchMethodException | SecurityException e) {
      try {
        return cls.getMethod(name, new Class<?>[] { or });
      } catch (NoSuchMethodException | SecurityException ex) {
        String msg = String.format("%s should implement %s(%s) / %s(%s)", cls.getName(), name,
            either.getName(), cls.getName(), or.getName());
        fail(msg);
      }
    }
    return null;
  }

  private static Constructor<?> shouldHaveTakesEitherConstructor(Class<?> cls, Class<?> either,
      Class<?> or) {
    try {
      return cls.getConstructor(new Class<?>[] { either });
    } catch (NoSuchMethodException | SecurityException e) {
      try {
        return cls.getConstructor(new Class<?>[] { or });
      } catch (NoSuchMethodException | SecurityException ex) {
        String msg = String.format("%s should have constructor %s(%s) / %s(%s)", cls.getName(),
            cls.getName(), either.getName(), cls.getName(), or.getName());
        fail(msg);
      }
    }
    return null;
  }

  public static void shouldImplementInterface(Class<?> cls, Class<?> inter) {
    assertTrue(String.format("%s should implement interface %s", cls.getName(), inter.getName()),
        Arrays.asList(cls.getInterfaces()).contains(inter));
  }

  public static void shouldImplementGenericInterface(Class<?> cls, Class<?> inter) {
    assertTrue(String.format("%s should implement interface %s", cls.getName(), inter.getName()),
        Arrays.asList(cls.getGenericInterfaces()).contains(inter));
  }

  /**
   * Asserts that cls implements method name with parameters params.
   *
   * @param cls    class
   * @param name   method name
   * @param params parameters
   * @return the method, if it exists
   */
  public static Method shouldImplementMethod(Class<?> cls, String name, Class<?>[] params) {
    try {
      return cls.getDeclaredMethod(name, params);
    } catch (NoSuchMethodException | SecurityException e) {
      String msg = String.format("%s should implement %s(%s).", cls.getName(), name,
          paramsStr(params));
      fail(msg);
    }
    return null;
  }

  public static Class<?>[] shouldImplementNInterfaces(Class<?> cls, int n) {
    Class<?>[] interfaces = cls.getInterfaces();
    assertTrue(String.format("%s should implement %d interface(s)", cls.getName(), n),
        interfaces.length == n);
    return interfaces;
  }

  public static Method shouldImplementTakesBooleanMethod(Class<?> cls, String name) {
    return shouldImplementTakesEither(cls, Boolean.class, boolean.class, name);
  }

  public static Method shouldImplementTakesDoubleMethod(Class<?> cls, String name) {
    return shouldImplementTakesEither(cls, Double.class, double.class, name);
  }

  private static Method shouldImplementTakesEither(Class<?> cls, Class<?> either, Class<?> or,
      String name) {
    try {
      return cls.getDeclaredMethod(name, new Class<?>[] { either });
    } catch (NoSuchMethodException | SecurityException e) {
      try {
        return cls.getDeclaredMethod(name, new Class<?>[] { or });
      } catch (NoSuchMethodException | SecurityException ex) {
        String msg = String.format("%s should implement %s(%s) / %s(%s)", cls.getName(), name,
            either.getName(), name, or.getName());
        fail(msg);
      }
    }
    return null;
  }

  public static void shouldNotBeAbsrtact(Class<?> cls) {
    assertFalse(String.format("%s should not be an abstract class", cls.getName()),
        Modifier.isAbstract(cls.getModifiers()));
  }

  public static void shouldNotBeAbsrtact(Method method) {
    assertFalse(String.format("%s should not be an abstract method", method.getName()),
        Modifier.isAbstract(method.getModifiers()));
  }

  /**
   * Asserts that cls does not define any public methods (excludes inherited).
   *
   * @param cls class
   */
  public static void shouldNotDeclarePublicMethods(Class<?> cls) {
    Method[] methods = cls.getDeclaredMethods();
    String msg = String.format("%s should not implement any non-private methods.", cls.getName());
    for (Method method : methods) {
      if (!Modifier.isPrivate(method.getModifiers())) {
        fail(msg);
      }
    }
  }

  public static void shouldNotImplementInterfaces(Class<?> cls) {
    assertTrue(String.format("%s should not implement any interfaces", cls.getName()),
        cls.getInterfaces().length == 0);
  }

  /**
   * Asserts that cls does not implement method name with parameters params
   * (excludes inherited).
   *
   * @param cls    class
   * @param name   method name
   * @param params parameters
   */
  public static void shouldNotImplementMethod(Class<?> cls, String name, Class<?>[] params) {
    try {
      cls.getDeclaredMethod(name, params);
      String msg = String.format("%s should not implement %s(%s)", cls.getName(), name,
          paramsStr(params));
      fail(msg);
    } catch (NoSuchMethodException | SecurityException e) {
    }
  }

  public static void shouldReturn(Method method, String inClass, Class<?> cls) {
    assertTrue(String.format("%s in %s should return %s", method.getName(), inClass, cls.getName()),
        method.getReturnType().equals(cls));
  }

  public static void shouldReturnBoolean(Method method, String inClass) {
    shouldReturnEither(method, Boolean.class, boolean.class, inClass);
  }

  public static void shouldReturnDouble(Method method, String inClass) {
    shouldReturnEither(method, Double.class, double.class, inClass);
  }

  private static void shouldReturnEither(Method method, Class<?> either, Class<?> or,
      String inClass) {
    assertTrue(
        String.format("%s in %s should return %s/%s", method.getName(), inClass, either.getName(),
            or.getName()),
        method.getReturnType().equals(either) || method.getReturnType().equals(or));
  }
}
