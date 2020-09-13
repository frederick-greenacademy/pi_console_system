import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormControl, FormGroup, Validators, FormBuilder } from '@angular/forms';
import { first } from 'rxjs/operators';
import { AuthenticationHandler } from '../services/authentication.service'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  loading = false;
  submitted = false;
  returnUrl: string;
  username: string;
  password: string;
  title = 'pi-frontend';

  constructor(
    private formBuilder: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private authenHandler: AuthenticationHandler,
  ) {
    
  }

  ngOnInit() {

    // đòi hỏi thẩm định các ô nhập liệu
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  // dễ dàng truy cập các ô nhập liệu với một getter
  get f() { return this.loginForm.controls; }

  onSubmit() {
    this.submitted = true;

    if (this.loginForm.invalid) {
      return;
    }

    this.authenHandler.signin(this.f.username.value, this.f.password.value).pipe(first()).subscribe(data => {
      console.log('My Data:', data)
      if (data && data.account_id != undefined) {
        this.router.navigate(['/home'])
      } else {
        alert('Tên đăng nhập và mật khẩu không tìm thấy')
      }
    })
    
  }

}
