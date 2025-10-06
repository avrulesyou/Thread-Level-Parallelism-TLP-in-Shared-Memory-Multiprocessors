#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdint.h>
#include "gem5/m5ops.h"

// Define the vector size and number of threads.
// NUM_THREADS can be overridden at compile time e.g., gcc -DNUM_THREADS=4
#ifndef NUM_THREADS
#define NUM_THREADS 4
#endif
#define VECTOR_SIZE 10240

// Global vectors and scalar alpha
double x[VECTOR_SIZE];
double y[VECTOR_SIZE];
double alpha = 2.0;

// Struct to pass arguments to each thread
typedef struct {
    int start_index;
    int end_index;
    int thread_id;
} thread_args_t;

// The DAXPY kernel function executed by each thread
void *daxpy_kernel(void *args) {
    thread_args_t *t_args = (thread_args_t *)args;
    for (int i = t_args->start_index; i < t_args->end_index; ++i) {
        y[i] = alpha * x[i] + y[i];
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    pthread_t threads[NUM_THREADS];
    thread_args_t thread_args[NUM_THREADS];
    int chunk_size = VECTOR_SIZE / NUM_THREADS;

    // Initialize vectors with some values
    for (int i = 0; i < VECTOR_SIZE; ++i) {
        x[i] = (double)i;
        y[i] = (double)(VECTOR_SIZE - i);
    }

    // --- Signal to gem5 to begin statistics collection ---
    m5_reset_stats(0, 0);

    // Create threads and assign each a portion of the workload
    for (int i = 0; i < NUM_THREADS; ++i) {
        thread_args[i].thread_id = i;
        thread_args[i].start_index = i * chunk_size;
        
        // Ensure the last thread handles any remaining elements
        if (i == NUM_THREADS - 1) {
            thread_args[i].end_index = VECTOR_SIZE;
        } else {
            thread_args[i].end_index = (i + 1) * chunk_size;
        }
        
        pthread_create(&threads[i], NULL, daxpy_kernel, &thread_args[i]);
    }

    // Wait for all threads to complete
    for (int i = 0; i < NUM_THREADS; ++i) {
        pthread_join(threads[i], NULL);
    }

    // --- Signal to gem5 to dump stats and exit simulation ---
    m5_dump_stats(0, 0);
    m5_exit(0);

    return 0; // This part is not reached in simulation
}
