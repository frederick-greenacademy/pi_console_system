import { Injectable } from '@angular/core';
import { from } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { map } from 'rxjs/operators';
import { Account } from '../models/account'

@Injectable({
  providedIn: 'root'
})
export class AccountHandler {

  private urlForUploadFiles = 'http://192.168.0.101:8000/upload/files'
  private urlForEnrollInfo = 'http://192.168.0.101:8000/api/register'

  private isCompleteEnrollSubject: BehaviorSubject<boolean>;
  public isCompleteEnroll: Observable<boolean>;
  private isLoadingSubject: BehaviorSubject<boolean>;
  public isLoading: Observable<boolean>;

  enrollInfo: Account
  capturedImages: File[] = []

  constructor(
    private http: HttpClient) {
    this.isCompleteEnrollSubject = new BehaviorSubject(false)
    this.isCompleteEnroll = this.isCompleteEnrollSubject.asObservable()
    this.isLoadingSubject = new BehaviorSubject(false)
    this.isLoading = this.isLoadingSubject.asObservable()

  }

  enroll(acc: Account) {
    this.enrollInfo = acc
  }

  register() {

    const enrollForm = new FormData()
    enrollForm.append('first_name', this.enrollInfo.first_name)
    enrollForm.append('last_name', this.enrollInfo.last_name)
    enrollForm.append('user_name', this.enrollInfo.user_name)
    enrollForm.append('password', this.enrollInfo.password)


    this.isLoadingSubject.next(true)

    let headers = new HttpHeaders()
    headers.append('Access-Control-Allow-Origin', '*');

    this.http.post<Account>(this.urlForEnrollInfo, enrollForm, { headers: headers }).subscribe(
      obj => {
        console.log('Phản hồi về ghi danh:', obj)
        if (obj["result"] == true) {

          let formUploadFiles = new FormData()
          let lengthOfImages = this.capturedImages.length
          formUploadFiles.append('number_image_files', lengthOfImages.toString())
          formUploadFiles.append('user_name', this.enrollInfo.user_name)

          for (let index = 0; index < lengthOfImages; index++) {
            formUploadFiles.append('files[]', this.capturedImages[index], 'file' + index + '.jpg')
          }
          this.uploadFiles(formUploadFiles)
        }
        else {
          this.isLoadingSubject.next(false)
          alert(obj["error"])
        }

      },
      (err) => {
        console.log('Lỗi ghi danh:', err)
        this.isLoadingSubject.next(false)
        alert(err)
      })

  }

  // register() {

  //   const enrollForm = new FormData()
  //   enrollForm.append('first_name', this.enrollInfo.first_name)
  //   enrollForm.append('last_name', this.enrollInfo.last_name)
  //   enrollForm.append('user_name', this.enrollInfo.user_name)
  //   enrollForm.append('password', this.enrollInfo.password)


  //   this.isLoadingSubject.next(true)

  //   this.http.post<any>(this.urlForEnrollInfo, enrollForm).pipe(map(obj => {
  //     console.log('Phản hồi về ghi danh:', obj)
  //     if (obj) {
  //       if (obj["result"] == true) {

  //         let formUploadFiles = new FormData()
  //         let lengthOfImages = this.capturedImages.length
  //         formUploadFiles.append('number_image_files', lengthOfImages.toString())
  //         formUploadFiles.append('user_name', this.enrollInfo.user_name)

  //         for (let index = 0; index < lengthOfImages; index++) {
  //           formUploadFiles.append('files[]', this.capturedImages[index], 'file' + index + '.jpg')
  //         }
  //         this.uploadFiles(formUploadFiles)
  //       }
  //       return "Đang tải ảnh đăng ký..."
  //     }
  //     this.isLoadingSubject.next(false)
  //     return "Hệ thống không thể ghi danh"
  //   }))

  // }

  addCapturedImage(image: File) {
    this.capturedImages.push(image)
    console.log('Trang thai cua isCompleteEnroll: ', this.capturedImages.length >= 6 ? true : false)
    this.isCompleteEnrollSubject.next(this.capturedImages.length >= 6 ? true : false)
  }

  private uploadFiles(formUploadFiles: FormData) {

    let headers = new HttpHeaders()
    headers.append('Content-Disposition', 'multipart/form-data');
    headers.append('Access-Control-Allow-Origin', '*');

    this.isLoadingSubject.next(true)

    this.http.post<any>(this.urlForUploadFiles, formUploadFiles, { headers: headers }).subscribe(
      res => {
        console.log('Phản hồi của tệp tải lên:', res)
        this.isLoadingSubject.next(false)
        alert('Hoàn tất việc ghi danh')
      },
      (err) => {
        console.log('Lỗi khi tải tệp lên:', err)
        this.isLoadingSubject.next(false)
      })
  }
}
