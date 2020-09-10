import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AppComponent } from './app.component'
import { from } from 'rxjs';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { ImageRegisterComponent } from './image-register/image-register.component'
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { AdminHomeComponent } from './login/admin-home/admin-home.component';
import { UserHomeComponent } from './login/user-home/user-home.component'
import { HomeComponent } from './home/home.component';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  {
    path: 'login', component: LoginComponent,
    children: [
      {
        path: 'admin',
        component: AdminHomeComponent
      }, 
      {
        path: 'user',
        component: UserHomeComponent
      }
    ]
  },
  {
    path: 'register', component: RegisterComponent,
    children: [
      // { path: '', redirectTo: 'register', pathMatch: 'full' },
      {
        path: 'image',
        component: ImageRegisterComponent
      }]
  },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }