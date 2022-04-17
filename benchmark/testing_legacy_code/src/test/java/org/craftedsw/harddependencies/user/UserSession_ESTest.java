/*
 * This file was automatically generated by EvoSuite
 * Mon May 31 14:04:59 GMT 2021
 */

package org.craftedsw.harddependencies.user;

import org.junit.Test;
import static org.junit.Assert.*;
import static org.evosuite.runtime.EvoAssertions.*;
import org.craftedsw.harddependencies.user.User;
import org.craftedsw.harddependencies.user.UserSession;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class UserSession_ESTest extends UserSession_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test0()  throws Throwable  {
      UserSession userSession0 = UserSession.getInstance();
      // Undeclared exception!
      try { 
        userSession0.isUserLoggedIn((User) null);
        fail("Expecting exception: RuntimeException");
      
      } catch(RuntimeException e) {
         //
         // UserSession.isUserLoggedIn() should not be called in an unit test
         //
         verifyException("org.craftedsw.harddependencies.user.UserSession", e);
      }
  }

  @Test(timeout = 4000)
  public void test1()  throws Throwable  {
      UserSession userSession0 = UserSession.getInstance();
      // Undeclared exception!
      try { 
        userSession0.getLoggedUser();
        fail("Expecting exception: RuntimeException");
      
      } catch(RuntimeException e) {
         //
         // UserSession.getLoggedUser() should not be called in an unit test
         //
         verifyException("org.craftedsw.harddependencies.user.UserSession", e);
      }
  }
}