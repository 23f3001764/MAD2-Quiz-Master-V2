import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/components/HomeView.vue'
import UserLogin from '@/components/UserLogin.vue'
import UserLogup from '@/components/UserLogup.vue'
import AdminSubject from '@/components/AdminSubject.vue'
import AddSubject from '@/components/AddSubject.vue'
import EditSubject from '@/components/EditSubject.vue'
import AdminChapter from '@/components/AdminChapter.vue'
import AddChapter from '@/components/AddChapter.vue'
import EditChapter from '@/components/EditChapter.vue'
import AdminQuiz from '@/components/AdminQuiz.vue'
import AddQuiz from '@/components/AddQuiz.vue'
import EditQuiz from '@/components/EditQuiz.vue'
import AdminQuestion from '@/components/AdminQuestion.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: UserLogin,
    },
    {
      path: '/signup',
      name: 'signup',
      component: UserLogup,
    },
    {
      path: '/adminsubject',
      name: 'adminsubject',
      component: AdminSubject,
    },
    {
      path: '/addsubject',
      name: 'addsubject',
      component: AddSubject,
    },
    {
      path: '/editsubject/:id',
      name: 'editsubject',
      component: EditSubject,
    },
    {
      path: '/editchapter/:id',
      name: 'editchapter',
      component: EditChapter,
    },
    {
      path: '/adminchapter/:sname',
      name: 'adminchapter',
      component: AdminChapter,
    },
    {
      path: '/adminquiz/:chname',
      name: 'adminquiz',
      component: AdminQuiz,
    },
    {
      path: '/addchapter/:sname',
      name: 'addchapter',
      component: AddChapter,
    },
    {
      path: '/addquiz/:chname',
      name: 'addquiz',
      component: AddQuiz,
    },
    {
      path: '/editquiz/:id',
      name: 'editquiz',
      component: EditQuiz,
    },
    {
      path: '/adminquestion/:quiz_id',
      name: 'adminquestion',
      component: AdminQuestion,
    },
  ],
})

export default router
