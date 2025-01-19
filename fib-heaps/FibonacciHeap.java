import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

/**
 * FibonacciHeap
 *
 * An implementation of Fibonacci heap over positive integers.
 *
 */
public class FibonacciHeap
{
	public HeapNode min;
	public int Treenum;
	public int size;
	public int totalLink;
	public int totalcuts;
	/**
	 *
	 * Constructor to initialize an empty heap.
	 *
	 */
	public FibonacciHeap()
	{
		this.min=null;
		this.Treenum=0;
		this.size=0;
		this.totalLink=0;
		this.totalcuts=0;
	}

	/**
	 * 
	 * pre: key > 0
	 *
	 * Insert (key,info) into the heap and return the newly generated HeapNode.
	 *
	 */
	public HeapNode insert(int key, String info) //O(1)
	{    
		HeapNode newnode= new HeapNode(key, info);
		if(this.min==null){
			this.min=newnode;
			this.min.next=this.min;
			this.min.prev=this.min;
		}
		else{
			newnode.next=this.min;
			newnode.prev=this.min.prev;
			this.min.prev.next=newnode;
			this.min.prev=newnode;
			if(this.min.key>key)
				this.min=newnode;
		}
		this.Treenum++;
		this.size++;
		return newnode;
	}

	/**
	 * 
	 * Return the minimal HeapNode, null if empty.
	 *
	 */
	public HeapNode findMin()
	{
		return this.min;
	}

	/**
	 * 
	 * Delete the minimal item
	 *
	 */
	public void deleteMin()//O(n) wc, O(logn) amortized
	{
		if(this.min!=null){
		//first we delete min
			this.naiveDeletionOfMinNode();
			int maxRank = (int) Math.ceil(Math.log(this.size) / Math.log((1 + Math.sqrt(5)) / 2)); // log_phi(size)
			HeapNode[] treesarr = new HeapNode[Math.max((maxRank + 1),1)];//crearting rank array
			HeapNode pointer=this.min;
			if(pointer!=null){//starting successive linking
				treesarr[this.min.rank]=pointer;
				pointer=pointer.next;
				int treeschecked=1;//counts how many trees we visited and linked and/or put in treesarr
				int sumtrees=this.Treenum;
				while(treeschecked<sumtrees){
					int r=pointer.rank;//pointer's linked list rank
					HeapNode next=pointer.next;//saves the original next, so we will know from where to continue after successive linking
					while(treesarr[r]!=null){ //while there is a tree we can link pointer tree to
						pointer=this.Link(treesarr[r], pointer);
						treesarr[r]=null;
						r++;//updating linked tree rank for next while iteration
					}
					//after there is no other tree to link pointer tree to, we put pointer tree in his place in treesarr
					treesarr[r]=pointer;
					if(pointer.key<this.min.key)//updates min if needed
						this.min=pointer;
					treeschecked++;
					pointer=next;// pointer is now pointing to original next
				}
			}
		}
	}
	public void naiveDeletionOfMinNode(){ //O(logn)
		FibonacciHeap tmpheap=new FibonacciHeap();
		if(this.min.child!=null){//if min has children we want tmp heap to be his childrens list 
			HeapNode childrens=this.min.child;
			while(childrens.parent!=null){//updating childrens parent to be null, O(logn)= minode's rank 
				childrens.parent=null;
				this.totalcuts++;
				childrens=childrens.next;
			}
			//creating new tmp heap for min's childrens
			tmpheap.min=this.min.child;
			tmpheap.Treenum=this.min.rank;
		}
		//now because we have a pointer to min's childrens list we can delete min node and all his children from original heap (we dont update size because it stays the same-1)
		if(this.min.next==this.min)//if min is the only tree root in the heap
			this.min=null;
		else{
			this.min.next.prev=this.min.prev;
			this.min.prev.next=this.min.next;
			this.min=this.min.next;
		}
		this.Treenum--;
		this.size--;
		this.meld(tmpheap);//meld childrens heap with original heap wuthout min and his childrens 
	}

	public HeapNode Link(HeapNode node1, HeapNode node2){
		HeapNode minnode=node1;
		HeapNode newchild=node2;
		if(node1.key>node2.key){//we find the min node of the new tree
			minnode=node2;
			newchild=node1;
		}
		//first disconnect newchild from root's tree
		newchild.next.prev=newchild.prev;
		newchild.prev.next=newchild.next;
		if(minnode.child==null){//if rank of minnode=0
			minnode.child=newchild;
			newchild.next=newchild;
			newchild.prev=newchild;
		}
		else{//else we connect newchild to minnode's children linked list
			newchild.next=minnode.child;
			newchild.prev=minnode.child.prev;
			newchild.prev.next=newchild;
			minnode.child.prev=newchild;
		}
		newchild.parent=minnode;
		minnode.child=newchild;
		minnode.rank++;
		this.totalLink++;
		this.Treenum--;
		return minnode;
	}

	/**
	 * 
	 * pre: 0<diff<x.key
	 * 
	 * Decrease the key of x by diff and fix the heap. 
	 * 
	 */
	public void decreaseKey(HeapNode x, int diff) 
	{  
		if(x!=null){
			x.key=x.key-diff;
			if(x.parent!=null){//if x has parent
				if(x.parent.key>x.key){//check if stack rule is still holds
					HeapNode nodeparent=this.Cut(x);//if not we start cascading cuts
					while((nodeparent!=null)&&(nodeparent.mark)){
						nodeparent=this.Cut(nodeparent);
					}
					if(nodeparent!=null)//if we didnt make it to the root we need to mark the node
						nodeparent.mark=true;
				}
			}
			if(x.key<this.min.key)
				this.min=x;
		}
	}


	public HeapNode Cut(HeapNode x){
		HeapNode nodeparent=x.parent;//save pointer to original parent
		if(nodeparent!=null){
			if(nodeparent.child==x){//if child pointer of x's parent is x 
				if(x.next==x)//if x is the only child now parent has no children
					nodeparent.child=null;
				else//else xparent's child is the brother of x
					nodeparent.child=x.next;
			}
			//deleting x of parent's child list
			x.next.prev=x.prev;
			x.prev.next=x.next;
			//disconnecting x from his brothers and father :(
			x.next=x;
			x.prev=x;
			x.parent=null;
			//puting x in his own heap
			FibonacciHeap tmpheap= new FibonacciHeap();
			tmpheap.min=x;
			tmpheap.Treenum=1;
			//melding x heap with the original heap(tree num-is updating in meld func,size and all other invariants are not changing)
			this.meld(tmpheap);
			this.totalcuts++;//update total cuts
			nodeparent.rank--;//update parent's rank
	}
		return nodeparent;

	}

	/**
	 * 
	 * Delete the x from the heap.
	 *
	 */
	public void delete(HeapNode x) 
	{ 
		if(x!=null){
			int diff=x.key-this.min.key+1;
			HeapNode originalmin=this.min;
			this.decreaseKey(x, diff);
			this.naiveDeletionOfMinNode();
			this.min=originalmin;
		}
	}


	/**
	 * 
	 * Return the total number of links.
	 * 
	 */
	public int totalLinks()
	{
		return this.totalLink; 
	}


	/**
	 * 
	 * Return the total number of cuts.
	 * 
	 */
	public int totalCuts()
	{
		return totalcuts;
	}


	/**
	 * 
	 * Meld the heap with heap2
	 *
	 */
	public void meld(FibonacciHeap heap2)
	{
		
		if(heap2!=null){
			HeapNode othermin=heap2.findMin();
			if(this.min==null)
				this.min=othermin;
			else{
				if(othermin!=null){
				HeapNode minnext=this.min.next;
				HeapNode min2prev=othermin.prev;
				this.min.next=othermin;
				othermin.prev=this.min;
				minnext.prev=min2prev;
				min2prev.next=minnext;	 		
				if(this.min.key>othermin.key)
					this.min=othermin;
				}
			}
			this.size+=heap2.size();
			this.Treenum+=heap2.numTrees();
			this.totalLink+=heap2.totalLinks();
			this.totalcuts+=heap2.totalCuts();
			
		}	
	}

	/**
	 * 
	 * Return the number of elements in the heap
	 *   
	 */
	public int size()
	{
		return this.size;
	}


	/**
	 * 
	 * Return the number of trees in the heap.
	 * 
	 */
	public int numTrees()
	{
		return this.Treenum;
	}

	/**
	 * Class implementing a node in a Fibonacci Heap.
	 *  
	 */
	public static class HeapNode{
		public int key;
		public String info;
		public HeapNode child;
		public HeapNode next;
		public HeapNode prev;
		public HeapNode parent;
		public int rank;
		public boolean mark;

		public HeapNode(int key, String info){
			this.key=key;
			this.info=info;
			this.child=null;
			this.next=null;
			this.prev=null;
			this.parent=null;
			this.rank=0;
			this.mark=false;
		}
		public int getKey(){
			return this.key;
		}
	}
	public static class Expirement {
		public static int[] Buildrandarr(int n){
			List<Integer> lst=new ArrayList<>(n);
			for(int i=1;i<=n;i++){
				lst.add(i);
			}
			Collections.shuffle(lst);
			int[] arr=new int[lst.size()];
			for(int i=0;i<arr.length;i++){
				arr[i]=lst.get(i);
			}
			return arr;
		}
		public static FibonacciHeap InsertArrayToHeap(int[] arr){
			FibonacciHeap f=new FibonacciHeap();
			for(int i=0;i<arr.length;i++){
				f.insert(arr[i], "");
			}
			return f;
		}
		public static void Expirement1(int n,int i){
			int totaltime=0;
			int totalsize=0;
			int totalLink=0;
			int totalcuts=0;
			int totaltrees=0;
			for(int j=0;j<20;j++){
				int[] arr=Buildrandarr(n);
				long startTime = System.currentTimeMillis();
				FibonacciHeap f=InsertArrayToHeap(arr);
				f.deleteMin();
				long endtime=System.currentTimeMillis();
				totaltime+=endtime-startTime;
				totalsize+=f.size;
				totalLink+=f.totalLinks();
				totalcuts+=f.totalCuts();
				totaltrees+=f.numTrees();
			}
			System.out.println("expirement1 for i="+i);
			System.out.println("avg time "+totaltime/20);
			System.out.println("avg size "+totalsize/20);
			System.out.println("avg links "+totalLink/20);
			System.out.println("avg lcuts "+totalcuts/20);
			System.out.println("avg treenum "+totaltrees/20);
		}
		public static void Expirement2(int n,int i){
			int totaltime=0;
			int totalsize=0;
			int totalLink=0;
			int totalcuts=0;
			int totaltrees=0;
			for(int j=0;j<20;j++){
				int[] arr=Buildrandarr(n);
				long startTime = System.currentTimeMillis();
				FibonacciHeap f=InsertArrayToHeap(arr);
				for(int t=0;t<n/2;t++)
					f.deleteMin();
				long endtime=System.currentTimeMillis();
				totaltime+=endtime-startTime;
				totalsize+=f.size;
				totalLink+=f.totalLinks();
				totalcuts+=f.totalCuts();
				totaltrees+=f.numTrees();
			}
			System.out.println("expirement2 for i="+i);
			System.out.println("avg time "+totaltime/20);
			System.out.println("avg size "+totalsize/20);
			System.out.println("avg links "+totalLink/20);
			System.out.println("avg lcuts "+totalcuts/20);
			System.out.println("avg treenum "+totaltrees/20);
		}
		public static void Expirement3(int n,int i){
			int totaltime=0;
			int totalsize=0;
			int totalLink=0;
			int totalcuts=0;
			int totaltrees=0;
			for(int t=0;t<20;t++){
				int[] arr=Buildrandarr(n);
				long startTime = System.currentTimeMillis();
				HeapNode[] nodesarr=new HeapNode[arr.length];
				FibonacciHeap f=new FibonacciHeap();
				for(int j=0;j<arr.length;j++){
					nodesarr[arr[j]-1]=f.insert(arr[j], "");
				}
				f.deleteMin();
				int num=n;
				while(f.size()>(Math.pow(2,5 )-1)){
						f.delete(nodesarr[num-1]);
					num--;
				}
				long endtime = System.currentTimeMillis();
				totaltime+=(endtime-startTime);
				totalsize+=f.size;
				totalLink+=f.totalLinks();
				totalcuts+=f.totalCuts();
				totaltrees+=f.numTrees();
			}
			System.out.println("expirement3 for i="+i);
			System.out.println("avg time "+totaltime/20);
			System.out.println("avg size "+totalsize/20);
			System.out.println("avg links "+totalLink/20);
			System.out.println("avg lcuts "+totalcuts/20);
			System.out.println("avg treenum "+totaltrees/20);
	
		}
		public  static void Expirements(){
			for(int i=1;i<=5;i++){
				int n=(int) (Math.pow(3, i+7)-1);
				Expirement1(n, i);
				Expirement2(n, i);
				Expirement3(n, i);

			}
		}
		public static void main(String[] args){
			Expirements();
		}
	}

}
