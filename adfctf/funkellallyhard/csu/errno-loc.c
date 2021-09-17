#include <errno.h>
#include <tls.h>
int *
__errno_location (void)
{
  return &errno;
}
libc_hidden_def (__errno_location)
