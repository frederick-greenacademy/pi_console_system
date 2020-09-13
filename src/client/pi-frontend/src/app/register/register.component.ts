import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HostListener } from '@angular/core';
import { first } from 'rxjs/operators';
import { AuthenticationHandler } from '../services/authentication.service';


@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  registerForm: FormGroup;
  loading = false;
  submitted = false;
  isFinishedForm = false;

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private route: ActivatedRoute,
    private athenHandler: AuthenticationHandler
  ) {
    // // điều hướng về trang nguồn nếu chưa có thông tin đăng nhập
    // if (this.athenHandler.currentUser) {
    //   this.router.navigate(['/']);
    // }

  }

  @HostListener('window:popstate', ['$event'])
  onPopState(event: any) {
    this.isFinishedForm = false;
    this.router.navigate(['../'])
  }

  ngOnInit() {
    this.registerForm = this.formBuilder.group({
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  get f() { return this.registerForm.controls; }

  onSubmit() {
    this.submitted = true;

    // dừng tại đây nếu Biểu mẫu điền chưa được thẩm định
    if (this.registerForm.invalid) {
      return;
    }
    this.isFinishedForm = true;
    this.router.navigate(['register/image'])
  }

}
