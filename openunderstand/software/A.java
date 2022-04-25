class c1 {
    public int c1_p1;
    public double c1_p2;
    public int c1_p3;
    public int c1_p4;
    public void c1_f1 () {
        int localVar = c1_p4;
	    system.out.println("this is f1 of c1");
    }
    public void c1_f2 () {
	    system.out.println("this is f2 of c1");
    }
}

class c2 {
    public c1 clss_att;
    public int c2_p1;
    public int c2_p2;
    public void c2_f1 () {
	    system.out.println("this is f1 of c2");
    }
    public void c2_f2 () {
	    system.out.println("this is f2 of c2");
    }
    public void c2_f3 () {
	    system.out.println("this is f3 of c2");
    }
    public void c2_f4 () {
	    system.out.println("this is f4 of c2");
    }
}