#include<linux/syscalls.h>
#include<linux/kernel.h>
#include<linux/linkage.h>

#define MAXSIZE 500

int queue[MAXSIZE];
int front = 0;
int rear = 0;
int i, res = 0;

SYSCALL_DEFINE1(oslab_enqueue, int, a){
	
	if(rear >= MAXSIZE -1){ //if queue is full
		printk(KERN_INFO "[Error] - QUEUE IS FULL------------------\n");
		return -2;
	}
	else {
		for(i=0; i <= rear; i++){ //if 'a' is existing value and exception handler for input 0
			if(queue[i] == a && i != rear) {
				printk(KERN_INFO "[Error] - Already existing value\n");
				return -2; //if returns negative integer, syscall looks as error and return -1 which is known as errno(global variable)
			}
		}
	}
	printk(KERN_INFO "[System call] oslab_enqueue(); -----\n");
	queue[rear] = a; //put 'a' on the queue
	rear++; //move to next index
	printk("Queue Front------------------------\n");
	for(i=front; i<rear; i++) { //print queue from front to rear
		printk("%d\n", queue[i]);
	}
	printk("Queue Rear------------------------\n");

	return a;
}


SYSCALL_DEFINE0(oslab_dequeue){
	
	if(rear == front){ //if queue is empty
		printk(KERN_INFO "[Error] - EMPTY QUEUE------------\n");
		return -2;
	}

	printk(KERN_INFO "[System call] oslab_dequeue(); -------\n");
	res = queue[front]; //dequeue(take out) front 'a'
	front++; //move front to the next part
	printk("Queue Front---------------------\n");
	for(i = front; i<rear; i++) { //print queue from front to rear
		printk("%d\n", queue[i]);
	}
	printk("Queue Rear---------------------\n");

	return res;
}
