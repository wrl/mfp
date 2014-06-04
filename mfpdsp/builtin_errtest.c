#include <math.h>
#include <stdio.h>
#include <string.h>
#include <glib.h>
#include <sys/types.h>
#include <unistd.h>

#include "mfp_dsp.h"

typedef struct {
    int err_process;
    int err_destroy;
} errtest_data;

#define SEGFAULT() *(int *)0 = 0xdeadbeef

static int 
process(mfp_processor * proc) 
{
    errtest_data * d = (errtest_data *)proc->data;

    sprintf(mfp_last_activity, "errtest~ PROCESS: enter\n");
    printf("mfpdsp: errtest~ process()\n");
    if (d->err_process) {
        sprintf(mfp_last_activity, "errtest~ PROCESS: about to SIGSEGV\n");
        printf("errtest~: About to segfault in process(), PID=%d\n", getpid());
        SEGFAULT();
    }
    return 0;
}

static void 
init(mfp_processor * proc) 
{
    errtest_data * d = (errtest_data *)g_malloc0(sizeof(errtest_data));
    sprintf(mfp_last_activity, "errtest~ INIT\n");
    proc->data = (void *)d; 
    
    return;
}

static void
destroy(mfp_processor * proc) 
{
    errtest_data * d = (errtest_data *)proc->data;

    if (d->err_destroy) {
        sprintf(mfp_last_activity, "errtest~ DESTROY: about to SIGSEGV\n");
        printf("errtest~: About to segfault in destroy(), PID=%d\n", getpid());
        SEGFAULT();
    }
    return;
}

static int
config(mfp_processor * proc) 
{
    printf("mfpdsp: errtest~ config enter\n");
    errtest_data * d = (errtest_data *)(proc->data);
    gpointer err_config = g_hash_table_lookup(proc->params, "err_config");
    gpointer err_process = g_hash_table_lookup(proc->params, "err_process");
    gpointer err_destroy = g_hash_table_lookup(proc->params, "err_destroy");
    int errconf;

    sprintf(mfp_last_activity, "errtest~ CONFIG: enter\n");

    if (err_config != NULL) {
        if ((int)(*(float *)err_config)) { 
            sprintf(mfp_last_activity, "errtest~ CONFIG: about to SIGSEGV\n");
            printf("errtest~: About to segfault in config(), PID=%d\n", getpid());
            SEGFAULT();
            sprintf(mfp_last_activity, "errtest~ CONFIG: failed to SIGSEGV\n");
        }
    }

    if (err_process != NULL) {
        d->err_process = (int)(*(float *)err_process);
    }

    if (err_destroy != NULL) {
        d->err_destroy = (int)(*(float *)err_destroy);
    }

    return 1;
}

mfp_procinfo *  
init_builtin_errtest(void) {
    mfp_procinfo * p = g_malloc0(sizeof(mfp_procinfo));
    p->name = strdup("errtest~");
    p->is_generator = 1;
    p->process = process;
    p->init = init;
    p->destroy = destroy;
    p->config = config;
    p->params = g_hash_table_new_full(g_str_hash, g_str_equal, NULL, NULL);
    g_hash_table_insert(p->params, "err_config", (gpointer)PARAMTYPE_FLT);
    g_hash_table_insert(p->params, "err_process", (gpointer)PARAMTYPE_FLT);
    g_hash_table_insert(p->params, "err_destroy", (gpointer)PARAMTYPE_FLT);
    return p;
}
