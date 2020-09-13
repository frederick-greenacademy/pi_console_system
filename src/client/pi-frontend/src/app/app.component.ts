import { Component } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { first } from 'rxjs/operators';
import { AuthenticationHandler } from './services/authentication.service';
import { Account } from './models/account'
import { from } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  title = 'pi-frontend';
  user: Account = null
  
  constructor(
    private router: Router,
    private authenHandler: AuthenticationHandler
  ) {
    this.authenHandler.currentUser.subscribe(u => {
      if (u) {
        this.user = u
        this.router.navigate(['/home']);
      } else {
        this.user = null
        this.router.navigate(['/login']);
      }
    })
  }

  logout() {
    this.authenHandler.logout()
    this.router.navigate(['/']);
  }
} 
