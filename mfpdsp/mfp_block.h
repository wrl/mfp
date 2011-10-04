
#ifndef MFP_BLOCK_H
#define MFP_BLOCK_H

#include "mfp_dsp.h"

typedef struct {
	int blocksize;
	int allocsize;
	int aligned;
	float * data;
} mfp_block;

extern mfp_block * mfp_block_new(int blocsize);
extern void mfp_block_init(mfp_block * block, mfp_sample * data, int blocsize);
extern void mfp_block_free(mfp_block * in);

extern void mfp_block_resize(mfp_block * in, int newsize); 
extern int mfp_block_mul(mfp_block * in_1, mfp_block * in_2, mfp_block * out);
extern int mfp_block_add(mfp_block * in_1, mfp_block * in_2, mfp_block * out);
extern int mfp_block_fmod(mfp_block * in, mfp_sample constant, mfp_block * out);
extern int mfp_block_const_mul(mfp_block * in, mfp_sample constant, mfp_block * out);
extern int mfp_block_const_add(mfp_block * in, mfp_sample constant, mfp_block * out);
extern int mfp_block_index_fetch(mfp_block * indexes, mfp_sample * base, mfp_block * out); 
extern int mfp_block_zero(mfp_block * b); 
extern int mfp_block_fill(mfp_block * b, mfp_sample constant); 
extern mfp_sample mfp_block_ramp(mfp_block * b, mfp_sample init, mfp_sample incr); 
extern int mfp_block_mac(mfp_block * in_1, mfp_block * in_2, mfp_block * in_3, mfp_block * out);
extern int mfp_block_trunc(mfp_block * in, mfp_block * out); 
extern int mfp_block_copy(mfp_block * in, mfp_block * out);
extern mfp_sample mfp_block_prefix_sum(mfp_block * deltas, mfp_sample scale, 
		                              mfp_sample initval, mfp_block * out);

#endif
