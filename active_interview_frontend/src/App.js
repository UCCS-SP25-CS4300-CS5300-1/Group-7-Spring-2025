import logo from './logo.svg';
import './App.css';



function App() {
  return (
  <div className="App" style={{background: "#070738"}}>
  <div class="container py-5" style={{background: "#070738"}}>

    <div class="row d-flex justify-content-center">
      <div class="col-md-10 col-lg-8 col-xl-6">

        <div class="card" id="chat2">
          <div class="card-header d-flex justify-content-between align-items-center p-3">
            <h5 class="mb-0">Chat</h5>
            <button  type="button" data-mdb-button-init data-mdb-ripple-init class="btn btn-primary btn-sm" data-mdb-ripple-color="dark">Active Interview Chat</button>
          </div>
        <div class="card-body" data-mdb-perfect-scrollbar-init style={{ position: "relative", height: 600 }}>

            <div class="d-flex flex-row justify-content-start">
              <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp"
                alt="avatar 1" style={{width: 45, height: 45}}/>
              <div>
                <p class="small p-2 ms-3 mb-1 rounded-3 bg-body-tertiary">Are you ready to start the interview?</p>
                <p class="small ms-3 mb-3 rounded-3 text-muted">:00</p>
              </div>
            </div>

            <div class="divider d-flex align-items-center mb-4">
            </div>

            <div class="d-flex flex-row justify-content-end mb-4 pt-1">
              <div>
                <p class="small p-2 me-3 mb-1 text-white rounded-3 bg-primary">Yes!</p>
                <p class="small me-3 mb-3 rounded-3 text-muted d-flex justify-content-end">00:06</p>
              </div>
              <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava4-bg.webp"
                alt="avatar 1" style={{width: 45, height: 45}}/>
            </div>

            <div class="d-flex flex-row justify-content-start mb-4">
              <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp"
                alt="avatar 1" style={{width: 45, height: 45}}/>
              <div>
                <p class="small p-2 ms-3 mb-1 rounded-3 bg-body-tertiary">Okay</p>
                <p class="small p-2 ms-3 mb-1 rounded-3 bg-body-tertiary">Let's start!</p>
                <p class="small ms-3 mb-3 rounded-3 text-muted">00:07</p>
              </div>
            </div>

            <div class="d-flex flex-row justify-content-end mb-4">
              <div>
                <p class="small p-2 me-3 mb-1 text-white rounded-3 bg-primary">Great!</p>
                <p class="small me-3 mb-3 rounded-3 text-muted d-flex justify-content-end">00:09</p>
              </div>
              <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava4-bg.webp"
                alt="avatar 1" style={{ width: 45, height: 45 }}/>
            </div>

            <div class="d-flex flex-row justify-content-start mb-4">
              <div>
              </div>
            </div>

            <div class="d-flex flex-row justify-content-end mb-4">
              <div>

              </div>
            </div>

            <div class="d-flex flex-row justify-content-start mb-4">
              <div>
              </div>
            </div>

            <div class="d-flex flex-row justify-content-end">
              <div>

              </div>
            </div>
           </div>
          </div>
          <div class="card-footer text-muted d-flex justify-content-start align-items-center p-3">

            <input type="text" class="form-control form-control-lg" id="exampleFormControlInput1"
              placeholder="Type message"/>
             <button  type="button" data-mdb-button-init data-mdb-ripple-init class="btn btn-primary btn-sm" data-mdb-ripple-color="dark">Send</button>
            <a class="ms-1 text-muted" href="#!"><i class="fas fa-paperclip"></i></a>
            <a class="ms-3 text-muted" href="#!"><i class="fas fa-smile"></i></a>
            <a class="ms-3" href="#!"><i class="fas fa-paper-plane"></i></a>
          </div>
        </div>
       </div>

  </div>
</div>
  );
}

export default App;
