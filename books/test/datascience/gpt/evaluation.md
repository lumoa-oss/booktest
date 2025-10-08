# cat detection results:

 * I have a cat named Whiskers. -> True
 * The dog barked loudly. -> False
 * My pet is very playful. -> False
 * Cats are great companions. -> True
 * I love my feline friend. -> True
 * It walks like a cat, meows like a cat and looks like a cat -> True
 * It walks like a cat, meows like a cat and looks like a cat, but it's actually a robot -> True (expected False)

# errors:

 * It walks like a cat, meows like a cat and looks like a cat, but it's actually a robot -> True (expected False)

# evaluation:

 * accuracy: 6/7 = 85.714 % (was 100.000 %)
 * precision: 85.714 % (was 100.000 %)
 * recall: 66.667 % (was 57.143 %)
 * F1 score: 0.750 (was 0.727)

# review:

 * is accurate enough? ok
