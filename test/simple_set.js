scope({c0_A:3, c0_B:3});
defaultScope(1);
intRange(-8, 7);

c0_B = Clafer("c0_B").withCard(3, 3);
c0_A = Clafer("c0_A").withCard(3, 3);
c0_A.refToUnique(c0_B);
