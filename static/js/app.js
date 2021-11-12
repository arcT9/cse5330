$.noConflict();
jQuery(document).ready(function ($) { 

    $.ajax({
        url: '/getUsers',
        dataType: 'json',
        success: function (data) {
            options = '<option disabled selected>Select User Name</option>'
            var $user_select = $('.user_select')
            data.forEach(user => {
                options += `<option id=${user.id} value=${user.id}>${user.name}</option>`
            });
            $user_select.html(options);
        }
    });

    $.ajax({
        url: '/getRoles',
        dataType: 'json',
        success: function (data) {
            options = '<option disabled selected>Select Role Name</option>'
            var $user_select = $('.role_select')
            data.forEach(role => {
                options += `<option id=${role.id} value=${role.id}>${role.name}</option>`
            });
            $user_select.html(options);
        }
    });

    $.ajax({
        url: '/getPrivileges',
        dataType: 'json',
        success: function (data) {
            options = '<option disabled selected>Select Privilege Name</option>'
            var $privilege_select = $('.privilege_select')
            data.forEach(privilege => {
                options += `<option id=${privilege.id} value=${privilege.id}>${privilege.name}</option>`
            });
            $privilege_select.html(options);
        }
    });

    $('#user_privilege_dropdown').on('change', function () {
        $.ajax({
            url: '/checkPrivilege/' + this.value,
            dataType: 'json',
            success: function (data) {
                console.log(data)
                var $panel = $('#user_privileges_results_panel');
                var privileges = '';
                data.privileges.forEach(item => {
                    privileges += `<span class="label label-info">${item}</span> `
                })
                var tableData = '';
                if('owns' in data) {
                    tableData = `
                    <li class="list-group-item"
                    <h5>Owns</h5> : &nbsp;&nbsp; 
                    <strong class=''>${data.owns.join(', ')}</strong>
                </li>
                    `
                } else {
                    tableData = '';
                }
                var panel_data = `
                <li class="list-group-item"
                    <h5>Role</h5> : &nbsp;&nbsp; 
                    <strong class=''>${data.role}</strong>
                </li>
                ${tableData}
                <li class="list-group-item"
                    <h5>Privileges</h5> : &nbsp;&nbsp;
                    ${privileges}
                </li>
                `;
                $panel.html(panel_data);
            }
        });
    });

    $('#role_privilege_dropdown').on('change', function () {
        $.ajax({
            url: '/checkRolePrivilege/' + this.value,
            dataType: 'json',
            success: function (data) {
                console.log(data);
                var $p_panel = $('#role_privileges_results_panel');
                var privileges = '';
                if(data.privileges[0] != null) {
                    data.privileges[0].forEach(item => {
                        privileges += `<span class="label label-info">${item}</span> `
                    })
                } else {
                    privileges = 'None'
                }
                
                var usersData = ''
                if(data.users != null) {
                    usersData = `
                    <li class="list-group-item"
                    <h5>Users</h5> : &nbsp;&nbsp;
                    ${data.users.join(', ')}
                    </li>
                    `;
                } else {
                    usersData = `
                    <li class="list-group-item"
                    <h5>Users</h5> : &nbsp;&nbsp;
                    <strong>None</strong>
                    </li>
                    `;
                }
                var panel_data = `
                <li class="list-group-item"
                    <h5>Privileges</h5> : &nbsp;&nbsp; 
                    <strong class=''>${privileges}</strong>
                </li>
                ${usersData}
                `;
                $p_panel.html(panel_data);
            }
        });
    });

    $('#user_privilege_select').on('change', function () {
        var user_id = $('#user_privilege_select').val();
        var privilege_id = $('#privilege_privilege_select').val();
        $.ajax({
            url: `/checkUserPrivilege/${user_id}/${privilege_id}`,
            dataType: 'json',
            success: function (data) {
                var $panel = $('#boss_panel');
                $panel.removeClass("panel-default panel-success panel-danger");
                if(data == 'yes') {
                    $panel.addClass("panel-success");
                } else {
                    $panel.addClass("panel-danger");
                }
            }
        });
    });

    $('#privilege_privilege_select').on('change', function () {
        var user_id = $('#user_privilege_select').val();
        var privilege_id = $('#privilege_privilege_select').val();
        $.ajax({
            url: `/checkUserPrivilege/${user_id}/${privilege_id}`,
            dataType: 'json',
            success: function (data) {
                var $panel = $('#boss_panel');
                $panel.removeClass("panel-default panel-success panel-danger");
                if(data == 'yes') {
                    $panel.addClass("panel-success");
                } else {
                    $panel.addClass("panel-danger");
                }
            }
        });
    });

});