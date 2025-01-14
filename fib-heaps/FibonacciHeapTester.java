public class FibonacciHeapTester {
    public static void main(String[] args) {
        System.out.println("Starting FibonacciHeap Tester...");

        // יצירת FibonacciHeap חדש
        FibonacciHeap heap1 = new FibonacciHeap();
        FibonacciHeap heap2 = new FibonacciHeap();

        // הכנסת אלמנטים לערימה הראשונה
        System.out.println("\nInserting elements into heap1...");
        heap1.insert(10, "info10");
        heap1.insert(20, "info20");
        heap1.insert(5, "info5"); // זה המינימום
        heap1.insert(15, "info15");

        // הכנסת אלמנטים לערימה השנייה
        System.out.println("\nInserting elements into heap2...");
        heap2.insert(25, "info25");
        heap2.insert(2, "info2"); // זה המינימום בערימה השנייה
        heap2.insert(30, "info30");

        // בדיקת מינימום בשתי הערימות
        System.out.println("\nChecking minimums...");
        FibonacciHeap.HeapNode minNode1 = heap1.findMin();
        FibonacciHeap.HeapNode minNode2 = heap2.findMin();
        System.out.println("Heap1 minimum key: " + (minNode1 != null ? minNode1.getKey() : "null"));
        System.out.println("Heap2 minimum key: " + (minNode2 != null ? minNode2.getKey() : "null"));

        // בדיקת מספר העצים וגודל הערימה לפני meld
        System.out.println("\nHeap1 size before meld: " + heap1.size());
        System.out.println("Heap2 size before meld: " + heap2.size());
        System.out.println("Heap1 number of trees before meld: " + heap1.numTrees());
        System.out.println("Heap2 number of trees before meld: " + heap2.numTrees());

        // פעולת meld
        System.out.println("\nMelding heap1 and heap2...");
        heap1.meld(heap2);

        // בדיקות אחרי meld
        System.out.println("\nHeap1 size after meld: " + heap1.size());
        System.out.println("Heap1 number of trees after meld: " + heap1.numTrees());
        FibonacciHeap.HeapNode minAfterMeld = heap1.findMin();
        System.out.println("Heap1 minimum key after meld: " + (minAfterMeld != null ? minAfterMeld.getKey() : "null"));

        // מחיקת מינימום
        System.out.println("\nDeleting minimum from heap1...");
        int oldMin = heap1.findMin().getKey(); // שמירת המינימום הקודם
        heap1.deleteMin();
        FibonacciHeap.HeapNode newMin = heap1.findMin();
        System.out.println("Heap1 old minimum key: " + oldMin);
        System.out.println("Heap1 minimum key after deleteMin: " + (newMin != null ? newMin.getKey() : "null"));
        System.out.println("total links: " + heap1.totalLinks());
        System.out.println("total trees: " + heap1.numTrees());
        System.out.println("size " + heap1.size());

        // הכנסת אלמנטים נוספים לערימה הראשונה
        System.out.println("\nInserting more elements into heap1...");
        FibonacciHeap.HeapNode node40 = heap1.insert(40, "info40");
        FibonacciHeap.HeapNode node50 = heap1.insert(50, "info50");
        heap1.insert(22, "null");
        heap1.insert(18, "null");
        System.out.println("tree num " + heap1.numTrees());


        heap1.deleteMin();
        System.out.println("New minimum key after another delete min: " + heap1.findMin().getKey());
        System.out.println("tree num " + heap1.numTrees());
        System.out.println("links: " + heap1.totalLinks());
        // ביצוע decreaseKey
        System.out.println("\nPerforming decreaseKey on node50...");
        heap1.decreaseKey(node40, 39); // הערך החדש של node50 אמור להיות 1
        System.out.println("New minimum key after decreaseKey: " + heap1.findMin().getKey());
        System.out.println("total cuts " + heap1.totalCuts());
        System.out.println("size " + heap1.size());


    }
}
