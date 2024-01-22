<script setup>
import { Authenticator } from "@aws-amplify/ui-vue";
import { reactive, onMounted } from "vue";
import { fetchAuthSession } from "aws-amplify/auth";
import "@aws-amplify/ui-vue/styles.css";
import axios from "axios";

const API_URL =
  import.meta.env.VITE_VUE_APP_API_URL || "http://localhost:8000/api";

const createTaskForm = reactive({ title: "" });
const tasks = reactive({ openTasks: [], closedTasks: [] });

const clear_task_form = () => {
  createTaskForm.title = "";
};

const get_user_token = async () => {
  const token = (await fetchAuthSession()).tokens?.idToken?.toString();
  return { idToken: token };
};

const set_auth_token = async () => {
  const { idToken } = await get_user_token();
  const config = { headers: { Authorization: idToken } };
  return config;
};

const create_task = async () => {
  const response = await axios.post(
    `${API_URL}/create-task/`,
    {
      title: createTaskForm.title,
    },
    await set_auth_token()
  );
  clear_task_form();
  await list_open_tasks();
};

const list_open_tasks = async () => {
  const response = await axios.get(
    `${API_URL}/open-tasks/`,
    await set_auth_token()
  );
  tasks.openTasks = response.data.results;
};

const list_closed_tasks = async () => {
  const response = await axios.get(
    `${API_URL}/closed-tasks/`,
    await set_auth_token()
  );
  tasks.closedTasks = response.data.results;
};

const close_task = async (id) => {
  const response = await axios.post(
    `${API_URL}/close-task/`,
    { id: id },
    await set_auth_token()
  );
  await list_open_tasks();
  await list_closed_tasks();
};

onMounted(() => {
  list_open_tasks();
  list_closed_tasks();
});
</script>

<template>
  <authenticator username-alias="email" :login-mechanisms="['email']">
    <template v-slot="{ signOut }">
      <el-menu class="el-menu" mode="horizontal" :ellipsis="false">
        <div class="flex-grow" />
        <el-menu-item index="0" @click="signOut">Sign Out</el-menu-item>
      </el-menu>
      <el-row>
        <el-col :span="8" :offset="8">
          <el-card class="box-card">
            <el-form :model="createTaskForm" label-width="120px">
              <el-form-item label="Task Title">
                <el-input v-model="createTaskForm.title" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="create_task"
                  >Create</el-button
                >
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-card class="box-card">
            <template #header>
              <div class="card-header">
                <span>Open tasks</span>
              </div>
            </template>
            <el-table :data="tasks.openTasks">
              <el-table-column prop="title" label="Title" />
              <el-table-column fixed="right" label="Actions" width="120">
                <template #default="scope">
                  <el-button
                    link
                    type="primary"
                    size="large"
                    @click="close_task(scope.row.id)"
                    >Close</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="box-card">
            <template #header>
              <div class="card-header">
                <span>Closed tasks</span>
              </div>
            </template>
            <el-table :data="tasks.closedTasks">
              <el-table-column prop="title" label="Title" />
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </template>
  </authenticator>
</template>

<style lang="scss">
.flex-grow {
  flex-grow: 1;
}
</style>
