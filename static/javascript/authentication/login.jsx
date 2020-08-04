function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = $("[name='csrfmiddlewaretoken']").val();




class LoginComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            "username": "",
            "password": "",
            "error": ""
        }
    }

    update = () => {
        this.props.updateItem(this.state)
    }

    PasswordEncrypt = (password) => {
        var encrypt = new JSEncrypt();
        encrypt.setPublicKey($("[name='rsa_key']").val())
        return encrypt.encrypt(password)
    }

    SubmitForm = (e) => {
        const url = e.target.action
        e.preventDefault()
        let password = this.PasswordEncrypt(this.state.password)
        this.setState({password: password}, () => {
            var self = this
            $.ajax({
                url: url,
                method: "post",
                dataType: "json",
                headers: {"X-CSRFToken": csrftoken},
                data: this.state,
                success: function (data) {
                    let success = data.success
                    if (success) {
                        window.location = data.redirect
                    } else {
                        self.setState({error: data["msg"], password: ""})
                    }
                },
                error: function () {
                    self.setState({error: data["msg"], password: ""})
                }
            })
        })
    }
    HandleInput = (e) => {
        let name = e.target.name
        let value = e.target.value
        this.setState({[name]: value})
    }

    componentDidMount() {
        let errorMsg = $("[name='errorMsg']").val()
        if (errorMsg) {
            this.setState({error: errorMsg})
        }
    }

    render() {
        return (
            <div className="wrapper">
                <div className="page-wrapper">
                    <div className="container">
                        <div className="login-panel">
                            <div className="heading">
                                <img className={"pull-left"} src={"/static/images/logo/subex.png"}/>
                                <img className={"pull-right"} src={"/static/images/logo/secure.png"}/>
                            </div>
                            <div className="content">
                                <div className={""}>
                                    <form className="form-horizontal" action={window.location.pathname} onSubmit={this.SubmitForm}>
                                        <div className="form-group">
                                            <label className="control-label col-sm-2"
                                                   htmlFor="username">Username:</label>
                                            <div className="col-sm-10">
                                                <input type="text" className="form-control" id="username"
                                                       placeholder="Enter username"
                                                       name="username" onChange={this.HandleInput}/>
                                            </div>
                                        </div>
                                        <div className="form-group">
                                            <label className="control-label col-sm-2" htmlFor="pwd">Password:</label>
                                            <div className="col-sm-10">
                                                <input type="password" className="form-control" id="password"
                                                       placeholder="Enter password" name="password"
                                                       onChange={this.HandleInput} value={this.state.password}/>
                                            </div>
                                        </div>
                                        <div className="form-group">
                                            <div className=" col-sm-10 col-sm-offset-2">
                                                <button type="submit" className="btn btn-success btn-block">Login
                                                </button>
                                            </div>
                                        </div>
                                        <div
                                            className={"col-sm-10 col-sm-offset-2 " + (this.state.error !== "" ? "errorMessage" : "")}
                                            style={{paddingBottom: "10px"}}>{this.state.error}</div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className={"clearfix"}></div>
                </div>
            </div>
        );
    }
}

ReactDOM.render(<LoginComponent/>, document.getElementById('root'));