---
author: luo-kai
name: android-expert
description: Expert-level Android development with Kotlin and Jetpack Compose. Use when building Android apps, working with Jetpack Compose, ViewModel, LiveData, Room, Retrofit, Hilt, Coroutines, or publishing to the Play Store. Also use when the user mentions 'Jetpack Compose', 'ViewModel', 'Room', 'Hilt', 'Coroutines', 'Flow', 'Android build', 'Gradle', 'Play Store', or 'Android Studio'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Android Development Expert

You are an expert Android developer with deep knowledge of Kotlin, Jetpack Compose, MVVM architecture, Hilt dependency injection, and the modern Android development ecosystem.

## Before Starting

1. **UI framework** — Jetpack Compose or Views/XML?
2. **Min SDK** — API 24 (Android 7), 26, or higher?
3. **Architecture** — MVVM, MVI, Clean Architecture?
4. **Problem type** — building feature, debugging, performance, Play Store?
5. **DI framework** — Hilt, Koin, manual?

---

## Core Expertise Areas

- **Jetpack Compose**: composables, state hoisting, side effects, theming, navigation
- **ViewModel**: StateFlow, SharedFlow, LiveData, state management patterns
- **Coroutines**: launch, async, Flow, StateFlow, exception handling, dispatchers
- **Room**: entities, DAOs, migrations, TypeConverters, FTS
- **Hilt**: dependency injection, scopes, ViewModelComponent, testing
- **Retrofit + OkHttp**: API calls, interceptors, error handling, serialization
- **Navigation Compose**: nav graph, deep links, arguments, back stack
- **Play Store**: signing, AAB, release tracks, in-app updates, Play Console

---

## Key Patterns & Code

### App Architecture — MVVM with Clean Architecture
```
app/
  src/main/
    java/com/example/app/
      data/
        local/
          AppDatabase.kt
          dao/UserDao.kt
          entity/UserEntity.kt
        remote/
          ApiService.kt
          dto/UserDto.kt
        repository/
          UserRepositoryImpl.kt
      domain/
        model/User.kt
        repository/UserRepository.kt  (interface)
        usecase/GetUsersUseCase.kt
      presentation/
        users/
          UsersScreen.kt
          UsersViewModel.kt
          UsersUiState.kt
      di/
        AppModule.kt
        DatabaseModule.kt
        NetworkModule.kt
      MainActivity.kt
      App.kt
```

### Jetpack Compose — UI
```kotlin
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle

// Screen composable — stateless, receives state and callbacks
@Composable
fun UsersScreen(
    viewModel: UsersViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    UsersContent(
        uiState = uiState,
        onRefresh = viewModel::refresh,
        onUserClick = viewModel::onUserSelected,
        onDeleteUser = viewModel::deleteUser,
    )
}

@Composable
private fun UsersContent(
    uiState: UsersUiState,
    onRefresh: () -> Unit,
    onUserClick: (User) -> Unit,
    onDeleteUser: (User) -> Unit,
) {
    when {
        uiState.isLoading -> {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        }
        uiState.error != null -> {
            ErrorState(
                message = uiState.error,
                onRetry = onRefresh
            )
        }
        else -> {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(
                    items = uiState.users,
                    key = { it.id }  // stable keys for recomposition
                ) { user ->
                    UserCard(
                        user = user,
                        onClick = { onUserClick(user) },
                        onDelete = { onDeleteUser(user) },
                    )
                }
            }
        }
    }
}

@Composable
fun UserCard(
    user: User,
    onClick: () -> Unit,
    onDelete: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Card(
        onClick = onClick,
        modifier = modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = user.name,
                    style = MaterialTheme.typography.titleMedium,
                )
                Text(
                    text = user.email,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            IconButton(onClick = onDelete) {
                Icon(Icons.Default.Delete, contentDescription = 'Delete user')
            }
        }
    }
}
```

### ViewModel with StateFlow
```kotlin
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class UsersUiState(
    val users: List<User> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val selectedUser: User? = null,
)

sealed interface UsersEvent {
    data class ShowSnackbar(val message: String) : UsersEvent
    data class NavigateToDetail(val userId: String) : UsersEvent
}

@HiltViewModel
class UsersViewModel @Inject constructor(
    private val getUsersUseCase: GetUsersUseCase,
    private val deleteUserUseCase: DeleteUserUseCase,
) : ViewModel() {

    private val _uiState = MutableStateFlow(UsersUiState())
    val uiState: StateFlow<UsersUiState> = _uiState.asStateFlow()

    // One-time events (snackbars, navigation)
    private val _events = MutableSharedFlow<UsersEvent>()
    val events = _events.asSharedFlow()

    init {
        loadUsers()
    }

    private fun loadUsers() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            getUsersUseCase()
                .catch { error ->
                    _uiState.update {
                        it.copy(isLoading = false, error = error.message)
                    }
                }
                .collect { users ->
                    _uiState.update {
                        it.copy(isLoading = false, users = users)
                    }
                }
        }
    }

    fun refresh() = loadUsers()

    fun onUserSelected(user: User) {
        viewModelScope.launch {
            _events.emit(UsersEvent.NavigateToDetail(user.id))
        }
    }

    fun deleteUser(user: User) {
        viewModelScope.launch {
            try {
                deleteUserUseCase(user.id)
                _events.emit(UsersEvent.ShowSnackbar('User deleted'))
            } catch (e: Exception) {
                _events.emit(UsersEvent.ShowSnackbar('Failed to delete user'))
            }
        }
    }
}
```

### Room Database
```kotlin
import androidx.room.*
import kotlinx.coroutines.flow.Flow

// Entity
@Entity(tableName = 'users')
data class UserEntity(
    @PrimaryKey val id: String,
    val name: String,
    val email: String,
    val role: String,
    val createdAt: Long = System.currentTimeMillis(),
)

// DAO
@Dao
interface UserDao {
    @Query('SELECT * FROM users ORDER BY name ASC')
    fun observeAll(): Flow<List<UserEntity>>

    @Query('SELECT * FROM users WHERE id = :id')
    suspend fun findById(id: String): UserEntity?

    @Query('SELECT * FROM users WHERE role = :role')
    fun observeByRole(role: String): Flow<List<UserEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(user: UserEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(users: List<UserEntity>)

    @Delete
    suspend fun delete(user: UserEntity)

    @Query('DELETE FROM users WHERE id = :id')
    suspend fun deleteById(id: String)

    @Query('DELETE FROM users')
    suspend fun deleteAll()
}

// Database
@Database(
    entities = [UserEntity::class],
    version = 2,
    exportSchema = true,
)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao

    companion object {
        val MIGRATION_1_2 = object : Migration(1, 2) {
            override fun migrate(database: SupportSQLiteDatabase) {
                database.execSQL('ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT "user"')
            }
        }
    }
}

// TypeConverter for complex types
class Converters {
    @TypeConverter
    fun fromList(list: List<String>): String = list.joinToString(',') 

    @TypeConverter
    fun toList(value: String): List<String> = value.split(',').filter { it.isNotEmpty() }
}
```

### Hilt Dependency Injection
```kotlin
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import dagger.hilt.android.qualifiers.ApplicationContext
import android.content.Context
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            'app_database'
        )
        .addMigrations(AppDatabase.MIGRATION_1_2)
        .fallbackToDestructiveMigrationOnDowngrade()
        .build()
    }

    @Provides
    fun provideUserDao(db: AppDatabase): UserDao = db.userDao()
}

@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideOkHttpClient(authInterceptor: AuthInterceptor): OkHttpClient {
        return OkHttpClient.Builder()
            .addInterceptor(authInterceptor)
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = if (BuildConfig.DEBUG)
                    HttpLoggingInterceptor.Level.BODY
                else
                    HttpLoggingInterceptor.Level.NONE
            })
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        return Retrofit.Builder()
            .baseUrl(BuildConfig.API_BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(MoshiConverterFactory.create())
            .build()
    }

    @Provides
    @Singleton
    fun provideApiService(retrofit: Retrofit): ApiService {
        return retrofit.create(ApiService::class.java)
    }
}

// Bind interface to implementation
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    @Singleton
    abstract fun bindUserRepository(
        impl: UserRepositoryImpl
    ): UserRepository
}
```

### Navigation Compose
```kotlin
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.NavType
import androidx.navigation.navArgument
import androidx.navigation.navDeepLink

// Route definitions
sealed class Screen(val route: String) {
    object UserList   : Screen('users')
    object UserDetail : Screen('users/{userId}') {
        fun createRoute(userId: String) = 'users/$userId'
    }
    object Settings   : Screen('settings')
}

@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Screen.UserList.route,
    ) {
        composable(Screen.UserList.route) {
            UsersScreen(
                onUserClick = { userId ->
                    navController.navigate(Screen.UserDetail.createRoute(userId))
                }
            )
        }

        composable(
            route = Screen.UserDetail.route,
            arguments = listOf(
                navArgument('userId') { type = NavType.StringType }
            ),
            deepLinks = listOf(
                navDeepLink { uriPattern = 'https://example.com/users/{userId}' }
            ),
        ) { backStackEntry ->
            val userId = backStackEntry.arguments?.getString('userId')!!
            UserDetailScreen(
                userId = userId,
                onBack = { navController.navigateUp() }
            )
        }

        composable(Screen.Settings.route) {
            SettingsScreen(onBack = { navController.navigateUp() })
        }
    }
}
```

### Repository Pattern
```kotlin
interface UserRepository {
    fun observeUsers(): Flow<List<User>>
    suspend fun getUserById(id: String): User?
    suspend fun syncUsers()
    suspend fun deleteUser(id: String)
}

class UserRepositoryImpl @Inject constructor(
    private val userDao: UserDao,
    private val apiService: ApiService,
    private val dispatcher: CoroutineDispatcher = Dispatchers.IO,
) : UserRepository {

    // Expose DB as single source of truth
    override fun observeUsers(): Flow<List<User>> {
        return userDao.observeAll().map { entities ->
            entities.map { it.toDomain() }
        }
    }

    override suspend fun getUserById(id: String): User? = withContext(dispatcher) {
        userDao.findById(id)?.toDomain()
    }

    override suspend fun syncUsers() = withContext(dispatcher) {
        val users = apiService.getUsers()
        userDao.upsertAll(users.map { it.toEntity() })
    }

    override suspend fun deleteUser(id: String) = withContext(dispatcher) {
        apiService.deleteUser(id)
        userDao.deleteById(id)
    }
}

// Extension functions for mapping
fun UserEntity.toDomain() = User(id = id, name = name, email = email, role = role)
fun UserDto.toEntity() = UserEntity(id = id, name = name, email = email, role = role)
fun User.toEntity() = UserEntity(id = id, name = name, email = email, role = role)
```

### Gradle build.gradle.kts
```kotlin
// app/build.gradle.kts
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.kapt)
    alias(libs.plugins.hilt)
    alias(libs.plugins.kotlin.serialization)
}

android {
    namespace = 'com.example.app'
    compileSdk = 34

    defaultConfig {
        applicationId = 'com.example.app'
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = '1.0.0'
        buildConfigField('String', 'API_BASE_URL', '"https://api.example.com/"')
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile('proguard-android-optimize.txt'),
                'proguard-rules.pro'
            )
            signingConfig = signingConfigs.getByName('release')
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions { jvmTarget = '17' }

    buildFeatures {
        compose = true
        buildConfig = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = libs.versions.compose.compiler.get()
    }
}

dependencies {
    // Compose BOM — manages all Compose library versions
    val composeBom = platform(libs.androidx.compose.bom)
    implementation(composeBom)
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.compose.ui.tooling.preview)
    debugImplementation(libs.androidx.compose.ui.tooling)

    // Architecture
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.lifecycle.runtime.compose)
    implementation(libs.androidx.navigation.compose)
    implementation(libs.androidx.hilt.navigation.compose)

    // Hilt DI
    implementation(libs.hilt.android)
    kapt(libs.hilt.compiler)

    // Room
    implementation(libs.androidx.room.runtime)
    implementation(libs.androidx.room.ktx)
    kapt(libs.androidx.room.compiler)

    // Networking
    implementation(libs.retrofit)
    implementation(libs.retrofit.converter.moshi)
    implementation(libs.okhttp.logging.interceptor)

    // Coroutines
    implementation(libs.kotlinx.coroutines.android)
}
```

---

## Best Practices

- Use StateFlow for UI state — never mutable state directly in ViewModel
- Use SharedFlow for one-time events like navigation and snackbars
- Always collect flows with collectAsStateWithLifecycle — not collectAsState
- Use stable keys in LazyColumn items to prevent unnecessary recompositions
- Keep composables stateless — hoist state to ViewModel
- Use Room as single source of truth — sync from network, expose from DB
- Always use withContext(Dispatchers.IO) for database and network operations
- Use version catalog (libs.versions.toml) for dependency management

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| collectAsState() | Does not handle lifecycle properly | Use collectAsStateWithLifecycle() |
| Mutable state in ViewModel | External mutation breaks reactivity | Use MutableStateFlow with private backing property |
| Network on main thread | ANR (App Not Responding) | Use withContext(Dispatchers.IO) |
| No stable keys in LazyColumn | Full list recomposition on any change | Always provide key = { item.id } |
| Leaking ViewModel | Memory leak on configuration change | Use hiltViewModel() not manual instantiation |
| Missing @AndroidEntryPoint | Hilt injection fails silently | Annotate every Activity and Fragment |
| Coroutine in wrong scope | Cancelled when screen rotates | Use viewModelScope not GlobalScope |
| Hardcoded strings | Not translatable, bad practice | Use string resources |

---

## Related Skills

- **kotlin-expert**: For Kotlin language features and coroutines
- **react-native-expert**: For cross-platform mobile alternative
- **ios-expert**: For iOS counterpart patterns
- **cicd-expert**: For Android CI/CD with GitHub Actions
- **appsec-expert**: For Android security best practices
- **testing-expert**: For Compose UI testing and unit testing